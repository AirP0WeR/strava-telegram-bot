#  -*- encoding: utf-8 -*-

from datetime import date
from os import sys, path

from telegram import InlineKeyboardMarkup

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.clients.strava import StravaClient
from scripts.common.constants_and_variables import BotConstants
from scripts.common.operations import Operations
from scripts.commands.stats.ride_all_time import RideAllTimeStats
from scripts.commands.stats.ride_ytd import RideYtdStats
from scripts.commands.stats.run_all_time import RunAllTimeStats
from scripts.commands.stats.run_ytd import RunYtdStats
from scripts.commands.stats.ride_misc import RideMiscStats
from scripts.commands.stats.ride_all_time_hundreds import RideAllTimeHundredsStats
from scripts.commands.stats.ride_all_time_fifties import RideAllTimeFiftiesStats


class CalculateStats(object):

    def __init__(self, bot, update, user_data, athlete_token):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.athlete_token = athlete_token
        self.bot_constants = BotConstants()
        self.operations = Operations()

    def process(self):
        strava_client = StravaClient(self.athlete_token).get_client()
        athlete_info = strava_client.get_athlete()
        activities = strava_client.get_activities(after="1970-01-01T00:00:00Z")
        current_year = date.today().year

        ride_all_time_stats = RideAllTimeStats()
        ride_ytd_stats = RideYtdStats()
        ride_misc_stats = RideMiscStats()
        ride_all_time_fifties_stats = RideAllTimeFiftiesStats()
        ride_all_time_hundreds_stats = RideAllTimeHundredsStats()
        run_all_time_stats = RunAllTimeStats()
        run_ytd_stats = RunYtdStats()

        input_ride_all_time_stats = ride_all_time_stats.input()
        input_ride_ytd_stats = ride_ytd_stats.input()
        input_ride_misc_stats = ride_misc_stats.input()
        input_ride_all_time_fifties_serial_no, input_ride_all_time_fifties_message, input_ride_all_time_fifties_list = ride_all_time_fifties_stats.input()
        input_ride_all_time_hundreds_serial_no, input_ride_all_time_hundreds_message, input_ride_all_time_hundreds_list = ride_all_time_hundreds_stats.input()
        input_run_all_time_stats = run_all_time_stats.input()
        input_run_ytd_stats = run_ytd_stats.input()

        for activity in activities:
            if self.operations.is_activity_a_ride(activity):
                input_ride_all_time_stats = ride_all_time_stats.calculate(input_ride_all_time_stats, activity)
                input_ride_ytd_stats = ride_ytd_stats.calculate(input_ride_ytd_stats, activity, current_year)
                input_ride_misc_stats = ride_misc_stats.calculate(input_ride_misc_stats, activity)
                input_ride_all_time_fifties_serial_no, input_ride_all_time_fifties_message, input_ride_all_time_fifties_list = ride_all_time_fifties_stats.calculate(
                    input_ride_all_time_fifties_serial_no, input_ride_all_time_fifties_message,
                    input_ride_all_time_fifties_list, activity)
                input_ride_all_time_hundreds_serial_no, input_ride_all_time_hundreds_message, input_ride_all_time_hundreds_list = ride_all_time_hundreds_stats.calculate(
                    input_ride_all_time_hundreds_serial_no, input_ride_all_time_hundreds_message,
                    input_ride_all_time_hundreds_list, activity)
            elif self.operations.is_activity_a_run(activity):
                input_run_all_time_stats = run_all_time_stats.calculate(input_run_all_time_stats, activity)
                input_run_ytd_stats = run_ytd_stats.calculate(input_run_ytd_stats, activity, current_year)

        input_ride_all_time_fifties_list.append(input_ride_all_time_fifties_message)  # Add the remaining 50 km rides
        input_ride_all_time_hundreds_list.append(input_ride_all_time_hundreds_message)  # Add the remaining 100 km rides
        input_ride_misc_stats = ride_misc_stats.calculate_athlete_info(input_ride_misc_stats, athlete_info)

        stats = dict()
        stats['all_time_ride_stats'] = ride_all_time_stats.format(input_ride_all_time_stats)
        stats['ytd_ride_stats'] = ride_ytd_stats.format(input_ride_ytd_stats)
        stats['all_time_run_stats'] = run_all_time_stats.format(input_run_all_time_stats)
        stats['ytd_run_stats'] = run_ytd_stats.format(input_run_ytd_stats)
        stats['misc_ride_stats'] = ride_misc_stats.format(input_ride_misc_stats)
        stats['ride_all_time_fifties'] = input_ride_all_time_fifties_list
        stats['ride_all_time_hundreds'] = input_ride_all_time_hundreds_list

        for fifty in stats['ride_all_time_fifties']:
            self.update.message.reply_text(fifty, parse_mode="Markdown", disable_web_page_preview=True)

        for hundred in stats['ride_all_time_hundreds']:
            self.update.message.reply_text(hundred, parse_mode="Markdown", disable_web_page_preview=True)

        self.user_data['stats'] = stats
        self.update.message.reply_text(self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU,
                                       reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_MAIN_KEYBOARD_MENU))
