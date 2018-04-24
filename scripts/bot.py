#!/usr/bin/env python
import datetime
import json
import logging
import os
import sys
import time
from decimal import Decimal, ROUND_DOWN
from threading import Thread

import requests
import telegram
from telegram.ext import Updater, CommandHandler, Filters


class InitializeBot(object):

    def __init__(self):
        logging.info("Initializing %s" % self.__class__.__name__)

    @staticmethod
    def get_config():

        get_telegram_token = None

        config_path = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(config_path, 'config.json')
        with open(config_file, 'r') as f:
            config = json.load(f)

        environment = config['ENVIRONMENT']
        if environment == "PROD":
            get_telegram_token = config['PROD_TELEGRAM_BOT_TOKEN']
        elif environment == "DEV":
            get_telegram_token = config['DEV_TELEGRAM_BOT_TOKEN']
        get_athletes = config['ATHLETES']
        get_shadow_chat_id = int(config['SHADOW_MODE_CHAT_ID'])
        get_admin_user_name = config['ADMIN_USER_NAME']
        get_shadow_mode = config['SHADOW_MODE']

        return get_telegram_token, get_athletes, get_shadow_chat_id, get_admin_user_name, get_shadow_mode

    @staticmethod
    def strava_activity_hyperlink():
        return """[%s %s](https://www.strava.com/activities/%s)"""


class FormatValue(object):

    def __init__(self):
        logging.info("Initializing %s" % self.__class__.__name__)

    @staticmethod
    def meters_to_kilometers(distance):
        return float((Decimal(distance / 1000.0)).quantize(Decimal('.1'), rounding=ROUND_DOWN))

    @staticmethod
    def seconds_to_minutes(time_in_seconds):
        return time_in_seconds / 60

    @staticmethod
    def remove_decimal_point(number):
        return int(number)

    @staticmethod
    def seconds_to_human_readable(time_in_seconds):
        return str(datetime.timedelta(seconds=time_in_seconds))

    @staticmethod
    def date_to_human_readable(date):
        return time.strftime("%d/%m/%Y", time.strptime(date[:19], "%Y-%m-%dT%H:%M:%S"))

    @staticmethod
    def meters_per_second_to_kilometers(speed):
        return float((Decimal(speed * 3.6)).quantize(Decimal('.1'), rounding=ROUND_DOWN))


class StravaApi(object):

    def __init__(self, athlete_token):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.athlete_token = athlete_token

    def get_athlete_info(self):
        response = requests.get("https://www.strava.com/api/v3/athlete", headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()

    def get_athlete_stats(self, athlete_id):
        response = requests.get("https://www.strava.com/api/v3/athletes/%s/stats" % athlete_id,
                                headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()

    def get_athlete_activities(self, total_activities, page):
        response = requests.get(
            "https://www.strava.com/api/v3/athlete/activities?per_page=%s&page=%s" % (total_activities, page),
            headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()


class FitWit(StravaApi, FormatValue):

    def __init__(self, bot, update, athlete_token):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.bot = bot
        self.update = update
        StravaApi.__init__(self, athlete_token)

    @staticmethod
    def get_activity_type(activity_type):
        if activity_type == "Ride":
            return "C"
        else:
            return type

    def main(self):
        latest_activity = self.get_athlete_activities("1", "1")[0]
        message = "%s, %s, %s, %s" % (self.get_activity_type(latest_activity['type']),
                                      self.meters_to_kilometers(latest_activity['distance']),
                                      self.seconds_to_minutes(latest_activity['moving_time']),
                                      self.remove_decimal_point(latest_activity['kilojoules']))

        if latest_activity['has_heartrate']:
            message += "\nHR, %s, %s" % (self.remove_decimal_point(latest_activity['average_heartrate']),
                                         self.remove_decimal_point(latest_activity['max_heartrate']))

        message += "\n\nhttps://www.strava.com/activities/%s" % latest_activity['id']

        return message


class AthleteStats(StravaApi, FormatValue):

    def __init__(self, bot, update, athlete_token, command):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.bot = bot
        self.update = update
        self.command = command
        StravaApi.__init__(self, athlete_token)

    def calculate_stats(self, athlete_activities, stats):
        for activity in athlete_activities:
            if activity['type'] == 'Ride':
                distance = float(activity['distance'])
                if 50000.0 <= distance < 100000.0:
                    stats['fifties'] += 1
                elif 100000.0 <= distance < 150000.0:
                    stats['hundreds'] += 1
                elif 150000.0 < distance < 200000.0:
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
        period = message = None
        if self.command == "alltimestats":
            message = "*All Time Stats:*\n\n"
            period = "all_ride_totals"
        elif self.command == "ytdstats":
            message = "*Year to Date Stats:*\n\n"
            period = "ytd_ride_totals"

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
        logging.info("Initializing %s" % self.__class__.__name__)
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
                    message += "\n\t\t\t\t\t\t\t\t\t\t\t\t %s (%s kms)" % (
                        bike['name'], self.meters_to_kilometers(bike['distance']))
        except Exception:
            pass
        return message

    @staticmethod
    def calculate_stats(athlete_activities, stats):
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

                if (activity['has_heartrate']) and (activity['max_heartrate'] > stats['max_heart_rate']):
                    stats['max_heart_rate'] = activity['max_heartrate']
                    stats['max_heart_rate_activity'] = activity['id']

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
            'max_heart_rate': 0,
            'max_heart_rate_activity': '',
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
        stats = self.get_stats()
        message = "*Fun Stats:*\n\n" \
                  "- _Max Power_: %s\n" \
                  "- _Best Average Power_: %s\n" \
                  "- _Max Speed_: %s\n" \
                  "- _Best Average Speed_: %s\n" \
                  "- _Best Avg Cadence_: %s\n" \
                  "- _Max Heart Rate_: %s\n" \
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
                  (strava_activity_hyperlink % (stats['max_watts'], 'watts', stats['max_watts_activity']),
                   strava_activity_hyperlink % (stats['average_watts'], 'watts', stats['average_watts_activity']),
                   strava_activity_hyperlink % (
                       self.meters_per_second_to_kilometers(stats['max_speed']), 'kph', stats['max_speed_activity']),
                   strava_activity_hyperlink % (self.meters_per_second_to_kilometers(stats['max_avg_speed']), 'kph',
                                                stats['max_avg_speed_activity']),
                   strava_activity_hyperlink % (
                       self.remove_decimal_point(stats['average_cadence']), '', stats['average_cadence_activity']),
                   strava_activity_hyperlink % (
                       self.remove_decimal_point(stats['max_heart_rate']), 'bpm', stats['max_heart_rate_activity']),
                   strava_activity_hyperlink % (
                       self.meters_to_kilometers(stats['biggest_ride']), 'kms', stats['biggest_ride_activity']),
                   strava_activity_hyperlink % (self.remove_decimal_point(stats['max_elevation_gain']), 'meters',
                                                stats['max_elevation_gain_activity']),
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


class StravaTelegramBot(object):

    def __init__(self):
        logging.info("Initializing %s" % self.__class__.__name__)

    @staticmethod
    def send_message(bot, update, message):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
        if shadow_mode and (shadow_chat_id != update.message.chat_id):
            bot.send_message(chat_id=shadow_chat_id, text=message, parse_mode="Markdown", disable_notification=True,
                             disable_web_page_preview=True)

    @staticmethod
    def get_athlete_token(bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        username = update.message.from_user.username
        if username in athletes.viewkeys():
            return {"Authorization": "Bearer " + athletes[username]}
        else:
            return False

    def handle_commands(self, bot, update, command):
        message = "Hi %s! You are not a registered user yet. Contact @panchambharadwaj for more details." % update.message.from_user.first_name
        athlete_token = self.get_athlete_token(bot, update)
        if athlete_token:

            if command == "start":
                message = "Hey %s! I'm your Strava Bot. Type '/' (backslash) to get the list of commands that I understand." % update.message.from_user.first_name

            elif command == "fw":
                greeting = "Hey %s! Give me a moment or two while I give your latest Strava activity in FitWit postable format." % update.message.from_user.first_name
                self.send_message(bot, update, greeting)
                message = FitWit(bot, update, athlete_token).main()

            elif command == "alltimestats" or command == "ytdstats":
                greeting = "Hey %s! Give me a moment or two while I give your stats." % update.message.from_user.first_name
                self.send_message(bot, update, greeting)
                message = AthleteStats(bot, update, athlete_token, command).main()

            elif command == "funstats":
                greeting = "Hey %s! Give me a minute or two while I give some of your fun stats." % update.message.from_user.first_name
                self.send_message(bot, update, greeting)
                message = FunStats(bot, update, athlete_token).main()

        self.send_message(bot, update, message)

    def start(self, bot, update):
        self.handle_commands(bot, update, "start")

    def fw(self, bot, update):
        self.handle_commands(bot, update, "fw")

    def alltimestats(self, bot, update):
        self.handle_commands(bot, update, "alltimestats")

    def ytdstats(self, bot, update):
        self.handle_commands(bot, update, "ytdstats")

    def funstats(self, bot, update):
        self.handle_commands(bot, update, "funstats")

    @staticmethod
    def error(update, error):
        logger.warning('Update "%s" caused error "%s"', update, error)

    def main(self):
        updater = Updater(telegram_token)
        dispatcher_handler = updater.dispatcher

        def stop_and_restart():
            updater.stop()
            os.execl(sys.executable, sys.executable, *sys.argv)

        def restart(bot, update):
            self.send_message(bot, update, "Bot is restarting...")
            Thread(target=stop_and_restart).start()

        dispatcher_handler.add_handler(CommandHandler("start", self.start))
        dispatcher_handler.add_handler(CommandHandler("fw", self.fw))
        dispatcher_handler.add_handler(CommandHandler("alltimestats", self.alltimestats))
        dispatcher_handler.add_handler(CommandHandler("ytdstats", self.ytdstats))
        dispatcher_handler.add_handler(CommandHandler("funstats", self.funstats))
        dispatcher_handler.add_handler(
            CommandHandler('restart', restart, filters=Filters.user(username=admin_user_name)))

        dispatcher_handler.add_error_handler(self.error)
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    initialize_bot = InitializeBot()
    telegram_token, athletes, shadow_chat_id, admin_user_name, shadow_mode = initialize_bot.get_config()
    strava_activity_hyperlink = initialize_bot.strava_activity_hyperlink()
    strava_telegram_bot = StravaTelegramBot()
    strava_telegram_bot.main()
