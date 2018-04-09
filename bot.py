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


class FitWit(StravaApi):
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
                                      (Decimal((Decimal(latest_activity['distance'] / 1000.0)).quantize(Decimal('.1'), rounding=ROUND_DOWN))),
                                      (latest_activity['moving_time']) / 60,
                                      int(latest_activity['kilojoules']))

        if latest_activity['has_heartrate']:
            message += "\nHR, %s, %s" % (int(latest_activity['average_heartrate']), int(latest_activity['max_heartrate']))

        message += "\n\nhttps://www.strava.com/activities/%s" % latest_activity['id']

        return message


class AthleteStats(StravaApi):
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
        return stats

    def get_stats(self, period):
        stats = {
            'fifties': 0,
            'hundreds': 0,
            'one_hundred_fifties': 0,
            'two_hundreds': 0,
            'rides': 0,
            'distance': 0,
            'moving_time': 0,
            'elevation_gain': 0
        }

        athlete_info = self.get_athlete_info()
        athlete_stats = self.get_athlete_stats(athlete_info['id'])

        stats['rides'] = athlete_stats[period]['count']
        stats['distance'] = Decimal((Decimal(athlete_stats[period]['distance'] / 1000.0)).quantize(Decimal('.1'), rounding=ROUND_DOWN))
        stats['moving_time'] = datetime.timedelta(seconds=athlete_stats[period]['moving_time'])
        stats['elevation_gain'] = Decimal((Decimal(athlete_stats[period]['elevation_gain'] / 1000.0)).quantize(Decimal('.1'), rounding=ROUND_DOWN))

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
        message += "_Rides_: %s\n_Distance_: %s kms\n_Moving Time_: %s hours\n_Elevation Gain_: %s kms\n_50's_: %s\n_100's_: %s (Includes %s _150's_ & %s _200's_)" % \
                   (stats['rides'], stats['distance'], stats['moving_time'], stats['elevation_gain'], stats['fifties'],
                    stats['hundreds'], stats['one_hundred_fifties'], stats['two_hundreds'])
        return message


class FunStats(StravaApi):
    def __init__(self, bot, update, athlete_token):
        self.bot = bot
        self.update = update
        StravaApi.__init__(self, athlete_token)

    def get_bikes_info(self, athlete_info):
        message = ""
        try:
            for bike in athlete_info['bikes']:
                if message == "":
                    message += "%s (%s kms)" % (bike['name'], Decimal((Decimal(bike['distance'] / 1000.0)).quantize(Decimal('.1'), rounding=ROUND_DOWN)))
                else:
                    message += "\n\t\t\t\t\t\t\t\t\t %s (%s kms)" % (bike['name'], Decimal((Decimal(bike['distance'] / 1000.0)).quantize(Decimal('.1'), rounding=ROUND_DOWN)))
        except Exception:
            pass
        return message

    def get_stats(self):
        stats = {
            'biggest_ride': 0,
            'biggest_climb': 0,
            'following': 0,
            'followers': 0,
            'strava_created': '',
            'bikes': ''
        }

        athlete_info = self.get_athlete_info()
        athlete_stats = self.get_athlete_stats(athlete_info['id'])

        stats['biggest_ride'] = Decimal((Decimal(athlete_stats['biggest_ride_distance'] / 1000.0)).quantize(Decimal('.1'), rounding=ROUND_DOWN))
        stats['biggest_climb'] = int(athlete_stats['biggest_climb_elevation_gain'])
        stats['following'] = athlete_info['friend_count']
        stats['followers'] = athlete_info['follower_count']
        stats['strava_created'] = time.strftime("%d/%m/%Y", time.strptime(athlete_info['created_at'][:19], "%Y-%m-%dT%H:%M:%S"))
        stats['bikes'] = self.get_bikes_info(athlete_info)

        return stats

    def main(self):
        greeting = "Hey %s! Give me a minute or two while I give some of your fun stats." % self.update.message.from_user.first_name
        send_message(self.bot, self.update, greeting)
        stats = self.get_stats()
        message = "*Fun Stats:*\n\n_Biggest Ride_: %s kms\n_Biggest Climb_: %s meters\n_Following Count_: %s\n_Followers Count_: %s\n_Using Strava Since_: %s\n_Bikes_: %s" % \
                  (stats['biggest_ride'], stats['biggest_climb'], stats['following'], stats['followers'],
                   stats['strava_created'], stats['bikes'])
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
    update.message.reply_text(message, parse_mode="Markdown")
    if shadow_mode:
        bot.send_message(chat_id=shadow_chat_id, text=message, parse_mode="Markdown", disable_notification=True)


def get_athlete_token(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
    username = update.message.from_user.username
    if athletes.has_key(username):
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
    main()
