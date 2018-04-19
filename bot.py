#!/usr/bin/env python
import requests
import telegram
import datetime
import json
import logging
import os
import sys
import time
from decimal import Decimal, ROUND_DOWN
from threading import Thread
from telegram.ext import Updater, CommandHandler, Filters


class StravaApi():
    def __init__(self, athlete_token):
        self.athlete_token = athlete_token

    def get_athlete_info(self):
        response = requests.get("https://www.strava.com/api/v3/athlete", headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()

    def get_athlete_stats(self, athlete_id):
        response = requests.get("https://www.strava.com/api/v3/athletes/%s/stats" % athlete_id, headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()

    def get_athlete_activities(self, total_activities, page):
        response = requests.get("https://www.strava.com/api/v3/athlete/activities?per_page=%s&page=%s" % (total_activities, page), headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()


class FormatValue():
    def meters_to_kilometers(self, distance):
        return (Decimal(distance/1000.0)).quantize(Decimal('.1'), rounding=ROUND_DOWN)

    def seconds_to_minutes(self, time):
        return time/60

    def remove_decimal_point(self, number):
        return int(number)

    def seconds_to_human_readable(self, time):
        return datetime.timedelta(seconds=time)

    def date_to_human_readable(self, date):
        return time.strftime("%d/%m/%Y", time.strptime(date[:19], "%Y-%m-%dT%H:%M:%S"))

    def meters_per_second_to_kilometers(self, speed):
        return (Decimal(speed * 3.6)).quantize(Decimal('.1'), rounding=ROUND_DOWN)


class FitWit(StravaApi, FormatValue):
    def __init__(self, bot, update, athlete_token):
        self.bot = bot
        self.update = update
        StravaApi.__init__(self, athlete_token)

    def get_activity_type(self, type):
        if type == "Ride":
            return "C"
        else:
            return type

    def main(self):
        message = "Hey %s! Give me a moment or two while I give your latest Strava activity in FitWit postable format." % self.update.message.from_user.first_name
        send_message(self.bot, self.update, message)
        latest_activity = self.get_athlete_activities("1", "1")[0]
        message = "%s, %s, %s, %s" % (self.get_activity_type(latest_activity['type']),
                                      self.meters_to_kilometers(latest_activity['distance']),
                                      self.seconds_to_minutes(latest_activity['moving_time']),
                                      self.remove_decimal_point(latest_activity['kilojoules']))

        if latest_activity['has_heartrate']:
            message += "\nHR, %s, %s" % (self.remove_decimal_point(latest_activity['average_heartrate']), self.remove_decimal_point(latest_activity['max_heartrate']))

        message += "\n\nhttps://www.strava.com/activities/%s" % latest_activity['id']

        return message


class AthleteStats(StravaApi, FormatValue):
    def __init__(self, bot, update, athlete_token, command):
        self.bot = bot
        self.update = update
        self.command = command
        StravaApi.__init__(self, athlete_token)

    def calculate_stats(self, athlete_activities, stats):
        for activity in athlete_activities:
            if activity['type'] == 'Ride':
                distance = float(activity['distance'])
                if distance >= 50000.0 and distance < 100000.0:
                    stats['fifties'] += 1
                elif distance >= 100000.0 and distance < 150000.0:
                    stats['hundreds'] += 1
                elif distance > 150000.0 and distance < 200000.0:
                    stats['one_hundred_fifties'] += 1
                    stats['hundreds'] += 1
                elif distance > 200000.0:
                    stats['two_hundreds'] += 1
                    stats['hundreds'] += 1

                if activity['trainer']:
                    stats['indoor_distance'] += self.meters_to_kilometers(activity['distance'])
                    stats['indoor_time'] += activity['moving_time']
                    stats['indoor_rides'] += 1

                if 'kilojoules' in activity:
                    stats['kilojoules'] += activity['kilojoules']

        return stats

    def get_stats(self, period):
        stats = {
            'rides': 0,
            'indoor_rides': 0,
            'distance': 0,
            'indoor_distance': 0,
            'moving_time': 0,
            'indoor_time': 0,
            'elevation_gain': 0,
            'kilojoules': 0.0,
            'fifties': 0,
            'hundreds': 0,
            'one_hundred_fifties': 0,
            'two_hundreds': 0
        }

        athlete_info = self.get_athlete_info()
        athlete_stats = self.get_athlete_stats(athlete_info['id'])

        stats['rides'] = athlete_stats[period]['count']
        stats['distance'] = self.meters_to_kilometers(athlete_stats[period]['distance'])
        stats['moving_time'] = self.seconds_to_human_readable(athlete_stats[period]['moving_time'])
        stats['elevation_gain'] = self.meters_to_kilometers(athlete_stats[period]['elevation_gain'])

        rides_count = athlete_stats[period]['count']
        if rides_count < 200:
            athlete_activities = self.get_athlete_activities(rides_count, "1")
            stats = self.calculate_stats(athlete_activities, stats)
        else:
            page = 1
            while page:
                athlete_activities = self.get_athlete_activities("200", page)
                if len(athlete_activities) == 0:
                    break
                stats = self.calculate_stats(athlete_activities, stats)
                page += 1

        return stats

    def main(self):
        if self.command == "alltimestats":
            time_adjective = "minute"
            header_adjective = "All Time stats"
            message = "*All Time Stats:*\n\n"
            period = "all_ride_totals"
        elif self.command == "ytdstats":
            time_adjective = "moment"
            header_adjective = "Year to Date stats"
            message = "*Year to Date Stats:*\n\n"
            period = "ytd_ride_totals"

        greeting = "Hey %s! Give me a %s or two while I give your %s." % (self.update.message.from_user.first_name, time_adjective, header_adjective)
        send_message(self.bot, self.update, greeting)
        stats = self.get_stats(period)
        message += "- _Rides_: %s (Includes %s Indoors)\n" \
                   "- _Distance_: %s kms (Includes %s kms of Indoors)\n" \
                   "- _Moving Time_: %s hours (Includes %s hours of Indoors)\n" \
                   "- _Elevation Gain_: %s kms\n" \
                   "- _Calories_: %s\n" \
                   "- _50's_: %s\n" \
                   "- _100's_: %s (Includes %s _150's_ & %s _200's_)" % \
                   (stats['rides'],
                    stats['indoor_rides'],
                    stats['distance'],
                    stats['indoor_distance'],
                    stats['moving_time'],
                    self.seconds_to_human_readable(stats['indoor_time']),
                    stats['elevation_gain'],
                    stats['kilojoules'],
                    stats['fifties'],
                    stats['hundreds'],
                    stats['one_hundred_fifties'],
                    stats['two_hundreds'])

        return message


class FunStats(StravaApi, FormatValue):
    def __init__(self, bot, update, athlete_token):
        self.bot = bot
        self.update = update
        StravaApi.__init__(self, athlete_token)

    def get_bikes_info(self, athlete_info):
        message = ""
        try:
            for bike in athlete_info['bikes']:
                if message == "":
                    message += "%s (%s kms)" % (bike['name'], self.meters_to_kilometers(bike['distance']))
                else:
                    message += "\n\t\t\t\t\t\t\t\t\t\t\t\t %s (%s kms)" % (bike['name'], self.meters_to_kilometers(bike['distance']))
        except Exception:
            pass
        return message

    def calculate_stats(self, athlete_activities, stats):
        for activity in athlete_activities:
            if activity['type'] == 'Ride':

                stats['kudos'] += activity['kudos_count']
                stats['achievement_count'] += activity['achievement_count']
                stats['break_time'] += activity['elapsed_time'] - activity['moving_time']

                if ('flagged' in activity) and (activity['flagged']):
                        stats['flagged'] += 1

                if ('private' in activity) and (activity['private']):
                        stats['private'] += 1

                if (activity['distance'] >= 70000.0) and ((activity['elapsed_time'] - activity['moving_time']) <= 900):
                        stats['non_stop'] += 1

                if activity['max_speed'] > stats['max_speed']:
                    stats['max_speed'] = activity['max_speed']
                    stats['max_speed_activity'] = activity['id']

                if activity['average_speed'] > stats['max_avg_speed']:
                    stats['max_avg_speed'] = activity['average_speed']
                    stats['max_avg_speed_activity'] = activity['id']

                if ('average_watts' in activity) and (activity['device_watts']):
                        if activity['average_watts'] > stats['average_watts']:
                            stats['average_watts'] = activity['average_watts']
                            stats['average_watts_activity'] = activity['id']
                        if activity['max_watts'] > stats['max_watts']:
                            stats['max_watts'] = activity['max_watts']
                            stats['max_watts_activity'] = activity['id']

                if (activity['has_heartrate']) and (activity['max_heartrate'] > stats['max_heartrate']):
                        stats['max_heartrate'] = activity['max_heartrate']
                        stats['max_heartrate_activity'] = activity['id']

                if ('average_cadence' in activity) and (activity['average_cadence'] > stats['average_cadence']):
                        stats['average_cadence'] = activity['average_cadence']
                        stats['average_cadence_activity'] = activity['id']

                if activity['distance'] > stats['biggest_ride']:
                    stats['biggest_ride'] = activity['distance']
                    stats['biggest_ride_activity'] = activity['id']

                if activity['total_elevation_gain'] > stats['max_elevation_gain']:
                    stats['max_elevation_gain'] = activity['total_elevation_gain']
                    stats['max_elevation_gain_activity'] = activity['id']

        return stats

    def get_stats(self):
        stats = {
            'biggest_ride': 0,
            'biggest_ride_activity': '',
            'max_elevation_gain': 0,
            'max_elevation_gain_activity': '',
            'non_stop': 0,
            'max_avg_speed': 0.0,
            'max_avg_speed_activity': '',
            'max_speed': 0.0,
            'max_speed_activity': '',
            'average_watts': 0.0,
            'average_watts_activity': '',
            'max_watts': 0,
            'max_watts_activity': '',
            'max_heartrate': 0,
            'max_heartrate_activity': '',
            'average_cadence': 0.0,
            'average_cadence_activity': '',
            'achievement_count': 0,
            'following': 0,
            'followers': 0,
            'strava_created': '',
            'private': 0,
            'flagged': 0,
            'break_time': 0,
            'kudos': 0,
            'bikes': ''
        }

        athlete_info = self.get_athlete_info()

        stats['following'] = athlete_info['friend_count']
        stats['followers'] = athlete_info['follower_count']
        stats['strava_created'] = self.date_to_human_readable(athlete_info['created_at'])
        stats['bikes'] = self.get_bikes_info(athlete_info)

        page = 1
        while page:
            athlete_activities = self.get_athlete_activities("200", page)
            if len(athlete_activities) == 0:
                break
            stats = self.calculate_stats(athlete_activities, stats)
            page += 1

        return stats

    def main(self):
        greeting = "Hey %s! Give me a minute or two while I give some of your fun stats." % self.update.message.from_user.first_name
        send_message(self.bot, self.update, greeting)
        stats = self.get_stats()
        message = "*Fun Stats:*\n\n" \
                  "- _Max Power_: %s\n" \
                  "- _Best Average Power_: %s\n" \
                  "- _Max Speed_: %s\n" \
                  "- _Best Average Speed_: %s\n" \
                  "- _Best Avg Cadence_: %s\n" \
                  "- _Max Heartrate_: %s\n" \
                  "- _Biggest Ride_: %s\n" \
                  "- _Max Elevation Gain_: %s\n" \
                  "- _Non-Stop Rides_: %s\n" \
                  "- _Total Break Time During Rides_: %s\n" \
                  "- _Using Strava Since_: %s\n" \
                  "- _Following Count_: %s\n" \
                  "- _Followers Count_: %s\n" \
                  "- _Kudos Received_: %s\n" \
                  "- _Total Achievements_: %s\n" \
                  "- _Private Rides_: %s\n" \
                  "- _Flagged Rides_: %s\n" \
                  "- _Bikes_: %s" % \
                  (activity_hyperlink % (stats['max_watts'], 'watts', stats['max_watts_activity']),
                   activity_hyperlink % (stats['average_watts'], 'watts', stats['average_watts_activity']),
                   activity_hyperlink % (self.meters_per_second_to_kilometers(stats['max_speed']), 'kmph', stats['max_speed_activity']),
                   activity_hyperlink % (self.meters_per_second_to_kilometers(stats['max_avg_speed']), 'kmph', stats['max_avg_speed_activity']),
                   activity_hyperlink % (self.remove_decimal_point(stats['average_cadence']), '', stats['average_cadence_activity']),
                   activity_hyperlink % (self.remove_decimal_point(stats['max_heartrate']), 'bpm', stats['max_heartrate_activity']),
                   activity_hyperlink % (self.meters_to_kilometers(stats['biggest_ride']), 'kms', stats['biggest_ride_activity']),
                   activity_hyperlink % (self.remove_decimal_point(stats['max_elevation_gain']), 'meters', stats['max_elevation_gain_activity']),
                   stats['non_stop'],
                   self.seconds_to_human_readable(stats['break_time']),
                   stats['strava_created'],
                   stats['following'],
                   stats['followers'],
                   stats['kudos'],
                   stats['achievement_count'],
                   stats['private'],
                   stats['flagged'],
                   stats['bikes'])

        return message


def get_config():
    with open('config.json', 'r') as f:
        config = json.load(f)

    environment = config['ENVIRONMENT']
    if environment == "PROD":
        telegram_token = config['PROD_TELEGRAM_BOT_TOKEN']
    elif environment == "DEV":
        telegram_token = config['DEV_TELEGRAM_BOT_TOKEN']
    athletes = config['ATHLETES']
    shadow_chat_id = config['SHADOW_MODE_CHAT_ID']
    admin_user_name = config['ADMIN_USER_NAME']
    shadow_mode = config['SHADOW_MODE']

    return telegram_token, athletes, shadow_chat_id, admin_user_name, shadow_mode


def send_message(bot, update, message):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
    if shadow_mode:
        bot.send_message(chat_id=shadow_chat_id, text=message, parse_mode="Markdown", disable_notification=True, disable_web_page_preview=True)


def get_athlete_token(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    username = update.message.from_user.username
    if username in athletes.viewkeys():
        return {"Authorization": "Bearer " + athletes[username]}
    else:
        return False


def handle_commands(bot, update, command):
    message = "Hi %s! You are not a registered user yet. Contact @panchambharadwaj for more details." % update.message.from_user.first_name
    athlete_token = get_athlete_token(bot, update)
    if athlete_token:

        if command == "start":
            message = "Hey %s! I'm your Strava Bot. Type '/' (backslash) to get the list of commands that I understand." % update.message.from_user.first_name

        elif command == "fw":
            message = FitWit(bot, update, athlete_token).main()

        elif command == "alltimestats" or command == "ytdstats":
            message = AthleteStats(bot, update, athlete_token, command).main()

        elif command == "funstats":
            message = FunStats(bot, update, athlete_token).main()

    send_message(bot, update, message)


def start(bot, update):
    handle_commands(bot, update, "start")


def fw(bot, update):
    handle_commands(bot, update, "fw")


def alltimestats(bot, update):
    handle_commands(bot, update, "alltimestats")


def ytdstats(bot, update):
    handle_commands(bot, update, "ytdstats")


def funstats(bot, update):
    handle_commands(bot, update, "funstats")


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(telegram_token)
    dispacther_handler = updater.dispatcher

    def stop_and_restart():
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(bot, update):
        send_message(bot, update, "Bot is restarting...")
        Thread(target=stop_and_restart).start()

    dispacther_handler.add_handler(CommandHandler("start", start))
    dispacther_handler.add_handler(CommandHandler("fw", fw))
    dispacther_handler.add_handler(CommandHandler("alltimestats", alltimestats))
    dispacther_handler.add_handler(CommandHandler("ytdstats", ytdstats))
    dispacther_handler.add_handler(CommandHandler("funstats", funstats))
    dispacther_handler.add_handler(CommandHandler('restart', restart, filters=Filters.user(username=admin_user_name)))

    dispacther_handler.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    telegram_token, athletes, shadow_chat_id, admin_user_name, shadow_mode = get_config()
    activity_hyperlink = """[%s %s](https://www.strava.com/activities/%s)"""
    main()