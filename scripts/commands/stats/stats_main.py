#  -*- encoding: utf-8 -*-

from os import sys, path

from telegram import InlineKeyboardMarkup

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.clients.strava import StravaClient
from scripts.commands.stats.calculate_stats import CalculateStats
from scripts.commands.stats.format_stats import FormatStats
from scripts.common.constants_and_variables import BotConstants


class StatsMain(object):

    def __init__(self, bot, update, user_data, athlete_token):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.athlete_token = athlete_token
        self.bot_constants = BotConstants()

    def process(self):
        strava_client = StravaClient(self.athlete_token).get_client()
        activities = strava_client.get_activities()
        athlete_info = strava_client.get_athlete()
        calculated_stats = CalculateStats(activities, athlete_info).main()
        formatted_stats = FormatStats(calculated_stats).main()
        self.user_data['stats'] = formatted_stats

        self.update.message.reply_text(self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU,
                                       reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_MAIN_KEYBOARD_MENU))
