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
        activities = strava_client.get_activities()
        current_year = date.today().year

        ride_all_time_stats = RideAllTimeStats()
        ride_ytd_stats = RideYtdStats()
        run_all_time_stats = RunAllTimeStats()
        run_ytd_stats = RunYtdStats()
        input_ride_all_time_stats = ride_all_time_stats.input()
        input_ride_ytd_stats = ride_ytd_stats.input()
        input_run_all_time_stats = run_all_time_stats.input()
        input_run_ytd_stats = run_ytd_stats.input()

        for activity in activities:
            if self.operations.is_activity_a_ride(activity):
                input_ride_all_time_stats = ride_all_time_stats.calculate(input_ride_all_time_stats, activity)
                input_ride_ytd_stats = ride_ytd_stats.calculate(input_ride_ytd_stats, activity, current_year)
            elif self.operations.is_activity_a_run(activity):
                input_run_all_time_stats = run_all_time_stats.calculate(input_run_all_time_stats, activity)
                input_run_ytd_stats = run_ytd_stats.calculate(input_run_ytd_stats, activity, current_year)

        stats = dict()
        stats['all_time_ride_stats'] = ride_all_time_stats.format(input_ride_all_time_stats)
        stats['ytd_ride_stats'] = ride_ytd_stats.format(input_ride_ytd_stats)
        stats['all_time_run_stats'] = run_all_time_stats.format(input_run_all_time_stats)
        stats['ytd_run_stats'] = run_ytd_stats.format(input_run_ytd_stats)

        self.user_data['stats'] = stats
        self.update.message.reply_text(self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU,
                                       reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_MAIN_KEYBOARD_MENU))
