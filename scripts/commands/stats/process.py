#  -*- encoding: utf-8 -*-

from datetime import timedelta
from os import sys, path

import psycopg2
from telegram import InlineKeyboardMarkup

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.constants_and_variables import BotConstants, BotVariables
from scripts.common.operations import Operations
from scripts.commands.stats.format import FormatStats


class ProcessStats(object):

    def __init__(self, bot, update, user_data, athlete_id):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.athlete_id = athlete_id
        self.bot_constants = BotConstants()
        self.bot_variables = BotVariables()
        self.operations = Operations()

    def get_strava_data(self):
        database_connection = psycopg2.connect(self.bot_variables.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(self.bot_constants.QUERY_GET_STRAVA_DATA.format(athlete_id=self.athlete_id))
        result = cursor.fetchone()
        cursor.close()
        database_connection.close()

        updated = (result[0] + timedelta(hours=5, minutes=30)).strftime("%d-%m-%Y %H:%M:%S")
        strava_data = result[1]

        return updated, strava_data

    def process(self):

        updated, strava_data = self.get_strava_data()

        if strava_data:

            format_stats = FormatStats(updated, strava_data)

            stats = dict()
            stats['all_time_ride_stats'] = format_stats.all_time_ride_stats()
            stats['ytd_ride_stats'] = format_stats.ytd_ride_stats()
            stats['py_ride_stats'] = format_stats.py_ride_stats()
            stats['cm_ride_stats'] = format_stats.cm_ride_stats()
            stats['pm_ride_stats'] = format_stats.pm_ride_stats()
            stats['all_time_run_stats'] = format_stats.all_time_run_stats()
            stats['ytd_run_stats'] = format_stats.ytd_run_stats()
            stats['py_run_stats'] = format_stats.py_run_stats()
            stats['cm_run_stats'] = format_stats.cm_run_stats()
            stats['pm_run_stats'] = format_stats.pm_run_stats()
            self.user_data['stats'] = stats
            self.update.message.reply_text(self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU,
                                           reply_markup=InlineKeyboardMarkup(
                                               self.bot_constants.STATS_MAIN_KEYBOARD_MENU))

        else:
            self.update.message.reply_text(self.bot_constants.MESSAGE_STATS_NOT_UPDATED, parse_mode="Markdown",
                                           disable_web_page_preview=True)
