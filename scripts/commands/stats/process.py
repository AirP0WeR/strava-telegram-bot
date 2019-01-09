#  -*- encoding: utf-8 -*-

from os import sys, path

from telegram import InlineKeyboardMarkup

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.commands.stats.calculate import CalculateStats
from scripts.common.constants_and_variables import BotConstants
from scripts.common.operations import Operations
from scripts.commands.stats.format import FormatStats


class ProcessStats(object):

    def __init__(self, bot, update, user_data, athlete_token):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.athlete_token = athlete_token
        self.bot_constants = BotConstants()
        self.operations = Operations()

    def process(self):
        calculate_stats = CalculateStats(self.bot, self.update, self.user_data, self.athlete_token)
        calculated_stats = calculate_stats.calculate()
        format_stats = FormatStats(calculated_stats)
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
                                       reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_MAIN_KEYBOARD_MENU))
