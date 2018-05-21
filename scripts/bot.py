#!/usr/bin/env python
import datetime
import json
import logging
import os
import sys
import time
from datetime import date
from decimal import Decimal, ROUND_DOWN
from threading import Thread

import dateutil.parser
import requests
import telegram
from telegram.ext import Updater, CommandHandler, Filters


class InitializeBot(object):

    def __init__(self):
        logging.info("Initializing %s" % self.__class__.__name__)

    @staticmethod
    def get_config():

        get_telegram_token = get_shadow_chat_id = None

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
        get_admin_user_name = config['ADMIN_USER_NAME']
        get_shadow_mode = config['SHADOW_MODE']
        if get_shadow_mode:
            get_shadow_chat_id = int(config['SHADOW_MODE_CHAT_ID'])

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
    def date_to_human_readable(activity_date):
        return time.strftime("%d/%m/%Y", time.strptime(activity_date[:19], "%Y-%m-%dT%H:%M:%S"))

    @staticmethod
    def meters_per_second_to_kilometers(speed):
        return float((Decimal(speed * 3.6)).quantize(Decimal('.1'), rounding=ROUND_DOWN))


class Common(object):
    def __init__(self):
        logging.info("Initializing %s" % self.__class__.__name__)

    @staticmethod
    def is_flagged_or_private(activity):
        if ('flagged' in activity) and (activity['flagged']):
            return True

        if ('private' in activity) and (activity['private']):
            return True

        return False


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

    def get_lastest_activity(self):
        response = requests.get("https://www.strava.com/api/v3/athlete/activities", data=[('per_page', '1')],
                                headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()[0]

    def update_activity_type(self, activity_id, activity_type):
        response = requests.put("https://www.strava.com/api/v3/activities/%s" % activity_id,
                                data=[('type', activity_type)], headers=self.athlete_token)
        if response.status_code == 200:
            return True
        else:
            return False


class AthleteStats(StravaApi, FormatValue, Common):

    def __init__(self, bot, update, athlete_token, command):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.bot = bot
        self.update = update
        self.command = command
        StravaApi.__init__(self, athlete_token)

    def calculate_stats(self, current_year, athlete_activities, all_time_stats, ytd_stats):
        for activity in athlete_activities:
            if not self.is_flagged_or_private(activity):
                if activity['type'] == 'Ride' or activity['type'] == 'VirtualRide':

                    activity_year = int((dateutil.parser.parse(activity['start_date_local'])).strftime('%Y'))

                    if activity_year == current_year:
                        ytd_stats['rides'] += 1
                    all_time_stats['rides'] += 1

                    if activity_year == current_year:
                        ytd_stats['moving_time'] += activity['moving_time']
                    all_time_stats['moving_time'] += activity['moving_time']

                    if activity_year == current_year:
                        ytd_stats['elevation_gain'] += activity['total_elevation_gain']
                    all_time_stats['elevation_gain'] += activity['total_elevation_gain']

                    distance = float(activity['distance'])

                    if activity_year == current_year:
                        ytd_stats['distance'] += distance
                    all_time_stats['distance'] += distance

                    if 50000.0 <= distance < 100000.0:
                        if activity_year == current_year:
                            ytd_stats['fifties'] += 1
                        all_time_stats['fifties'] += 1
                    elif 100000.0 <= distance < 150000.0:
                        if activity_year == current_year:
                            ytd_stats['hundreds'] += 1
                        all_time_stats['hundreds'] += 1
                    elif 150000.0 < distance < 200000.0:
                        if activity_year == current_year:
                            ytd_stats['one_hundred_fifties'] += 1
                            ytd_stats['hundreds'] += 1
                        all_time_stats['one_hundred_fifties'] += 1
                        all_time_stats['hundreds'] += 1
                    elif distance > 200000.0:
                        if activity_year == current_year:
                            ytd_stats['two_hundreds'] += 1
                            ytd_stats['hundreds'] += 1
                        all_time_stats['two_hundreds'] += 1
                        all_time_stats['hundreds'] += 1

                    if activity['trainer']:
                        if activity_year == current_year:
                            ytd_stats['indoor_distance'] += self.meters_to_kilometers(activity['distance'])
                            ytd_stats['indoor_time'] += activity['moving_time']
                            ytd_stats['indoor_rides'] += 1
                        all_time_stats['indoor_distance'] += self.meters_to_kilometers(activity['distance'])
                        all_time_stats['indoor_time'] += activity['moving_time']
                        all_time_stats['indoor_rides'] += 1

                    if 'kilojoules' in activity:
                        if activity_year == current_year:
                            ytd_stats['kilojoules'] += activity['kilojoules']
                        all_time_stats['kilojoules'] += activity['kilojoules']

        return all_time_stats, ytd_stats

    def get_stats(self, current_year):

        all_time_stats = {
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

        ytd_stats = {
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

        page = 1
        while page:
            athlete_activities = self.get_athlete_activities("200", page)
            if len(athlete_activities) == 0:
                break
            all_time_stats, ytd_stats = self.calculate_stats(current_year, athlete_activities, all_time_stats, ytd_stats)
            page += 1

        return all_time_stats, ytd_stats

    def main(self):

        all_time_stats, ytd_stats = self.get_stats(date.today().year)
        message = "*All Time Stats:*\n\n" \
                   "- _Rides_: %s (Includes %s Indoors)\n" \
                   "- _Distance_: %s kms (Includes %s kms of Indoors)\n" \
                   "- _Moving Time_: %s hours (Includes %s hours of Indoors)\n" \
                   "- _Elevation Gain_: %s kms\n" \
                   "- _Calories_: %s\n" \
                   "- _50's_: %s\n" \
                   "- _100's_: %s (Includes %s _150's_ & %s _200's_)\n\n" \
                   "*Year to Date Stats:*\n\n" \
                   "- _Rides_: %s (Includes %s Indoors)\n" \
                   "- _Distance_: %s kms (Includes %s kms of Indoors)\n" \
                   "- _Moving Time_: %s hours (Includes %s hours of Indoors)\n" \
                   "- _Elevation Gain_: %s kms\n" \
                   "- _Calories_: %s\n" \
                   "- _50's_: %s\n" \
                   "- _100's_: %s (Includes %s _150's_ & %s _200's_)" % \
                   (all_time_stats['rides'],
                    all_time_stats['indoor_rides'],
                    self.meters_to_kilometers(all_time_stats['distance']),
                    all_time_stats['indoor_distance'],
                    self.seconds_to_human_readable(all_time_stats['moving_time']),
                    self.seconds_to_human_readable(all_time_stats['indoor_time']),
                    self.meters_to_kilometers(all_time_stats['elevation_gain']),
                    all_time_stats['kilojoules'],
                    all_time_stats['fifties'],
                    all_time_stats['hundreds'],
                    all_time_stats['one_hundred_fifties'],
                    all_time_stats['two_hundreds'],
                    ytd_stats['rides'],
                    ytd_stats['indoor_rides'],
                    self.meters_to_kilometers(ytd_stats['distance']),
                    ytd_stats['indoor_distance'],
                    self.seconds_to_human_readable(ytd_stats['moving_time']),
                    self.seconds_to_human_readable(ytd_stats['indoor_time']),
                    self.meters_to_kilometers(ytd_stats['elevation_gain']),
                    ytd_stats['kilojoules'],
                    ytd_stats['fifties'],
                    ytd_stats['hundreds'],
                    ytd_stats['one_hundred_fifties'],
                    ytd_stats['two_hundreds'])

        return message


class FunStats(StravaApi, FormatValue, Common):

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
                    message += "\n\t\t\t\t\t\t\t\t\t\t\t\t\t %s (%s kms)" % (
                        bike['name'], self.meters_to_kilometers(bike['distance']))
        except KeyError, e:
            logging.info("Key error: %s" % e)
        return message

    def calculate_stats(self, athlete_activities, stats):
        for activity in athlete_activities:
            if not self.is_flagged_or_private(activity):
                if activity['type'] == 'Ride' or activity['type'] == 'VirtualRide':

                    stats['kudos'] += activity['kudos_count']
                    stats['achievement_count'] += activity['achievement_count']
                    stats['break_time'] += activity['elapsed_time'] - activity['moving_time']

                    if (activity['distance'] >= 70000.0) and (
                            (activity['elapsed_time'] - activity['moving_time']) <= 900):
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

            elif activity['type'] == 'Ride' or activity['type'] == 'VirtualRide':

                if ('flagged' in activity) and (activity['flagged']):
                    stats['flagged'] += 1

                if ('private' in activity) and (activity['private']):
                    stats['private'] += 1

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
                  "- _Flagged Rides_: %s\n" % \
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
                   stats['flagged'])

        if stats['bikes'] != "":
            message += "- _Bikes_: %s" % stats['bikes']

        return message


class UpdateActivity(StravaApi):

    def __init__(self, bot, update, activity_type, athlete_token):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.bot = bot
        self.update = update
        self.activity_type = activity_type
        StravaApi.__init__(self, athlete_token)

    def main(self):
        latest_activity = self.get_lastest_activity()
        if self.update_activity_type(latest_activity['id'], self.activity_type):
            return "Successfully updated your latest activity to Walk."
        else:
            return "Failed to update your latest activity to Walk."


class StravaTelegramBot(object):

    def __init__(self):
        logging.info("Initializing %s" % self.__class__.__name__)

    @staticmethod
    def send_message(bot, update, message):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
        if shadow_mode and (int(shadow_chat_id) != int(update.message.chat_id)):
            bot.send_message(chat_id=shadow_chat_id, text=message, parse_mode="Markdown", disable_notification=True,
                             disable_web_page_preview=True)
        else:
            logging.info("Chat ID & Shadow Chat ID are the same")

    @staticmethod
    def get_athlete_token(bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        username = update.message.from_user.username
        if username in athletes.viewkeys():
            return {"Authorization": "Bearer " + athletes[username]}
        else:
            return False

    def handle_commands(self, bot, update, command):
        message = "Hi %s! You are not a registered user yet. Contact %s for more details." \
                  % (update.message.from_user.first_name, admin_user_name)
        athlete_token = self.get_athlete_token(bot, update)
        if athlete_token:

            if command == "start":
                message = "Hey %s! I'm your Strava Bot. " \
                          "Type '/' to get the list of commands that I understand." \
                          % update.message.from_user.first_name

            elif command == "stats":
                greeting = "Hey %s! Give me a moment or two while I give your stats." \
                           % update.message.from_user.first_name
                self.send_message(bot, update, greeting)
                message = AthleteStats(bot, update, athlete_token, command).main()

            elif command == "funstats":
                greeting = "Hey %s! Give me a moment or two while I give some of your fun stats." \
                           % update.message.from_user.first_name
                self.send_message(bot, update, greeting)
                message = FunStats(bot, update, athlete_token).main()

            elif command == "updatetowalk":
                greeting = "Hey %s! Give me a moment while I update your latest activity to Walk." \
                           % update.message.from_user.first_name
                self.send_message(bot, update, greeting)
                message = UpdateActivity(bot, update, "Walk", athlete_token).main()

        self.send_message(bot, update, message)

    def start(self, bot, update):
        self.handle_commands(bot, update, "start")

    def stats(self, bot, update):
        self.handle_commands(bot, update, "stats")

    def funstats(self, bot, update):
        self.handle_commands(bot, update, "funstats")

    def updatetowalk(self, bot, update):
        self.handle_commands(bot, update, "updatetowalk")

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
        dispatcher_handler.add_handler(CommandHandler("stats", self.stats))
        dispatcher_handler.add_handler(CommandHandler("funstats", self.funstats))
        dispatcher_handler.add_handler(CommandHandler("updatetowalk", self.updatetowalk))
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
