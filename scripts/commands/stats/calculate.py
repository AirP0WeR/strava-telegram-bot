#  -*- encoding: utf-8 -*-

from datetime import date
from os import sys, path

from telegram import InlineKeyboardMarkup

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.clients.strava import StravaClient
from scripts.common.constants_and_variables import BotConstants
from scripts.common.operations import Operations
from scripts.commands.stats.input_and_output import InputStats, OutputStats
from scripts.commands.stats.ride_all_time import RideAllTimeStats


class CalculateStats(object):

    def __init__(self, bot, update, user_data, athlete_token):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.athlete_token = athlete_token
        self.bot_constants = BotConstants()
        self.operations = Operations()
        self.input_stats = InputStats()
        self.output_stats = OutputStats()

    def process(self):
        strava_client = StravaClient(self.athlete_token).get_client()
        athlete_info = strava_client.get_athlete()
        activities = strava_client.get_activities()
        current_year = date.today().year

        ride_all_time_stats = RideAllTimeStats()
        input_ride_all_time_stats = self.input_stats.INPUT_RIDE_ALL_TIME_STATS
        output_ride_all_time_stats = self.output_stats.OUTPUT_RIDE_ALL_TIME_STATS

        for activity in activities:
            if self.operations.is_activity_a_ride(activity):
                input_ride_all_time_stats = ride_all_time_stats.calculate(input_ride_all_time_stats, activity)

        output_ride_all_time_stats = ride_all_time_stats.format(input_ride_all_time_stats, output_ride_all_time_stats)

        self.user_data['stats']['all_time_ride_stats'] = output_ride_all_time_stats
        self.update.message.reply_text(self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU,
                                       reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_MAIN_KEYBOARD_MENU))
