#  -*- encoding: utf-8 -*-

import logging
import ujson
from collections import defaultdict

from clients.database import DatabaseClient
from clients.iron_cache import IronCache
from commands.stats.format import FormatStats
from common.constants_and_variables import BotConstants
from common.shadow_mode import ShadowMode


class Stats(object):

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_constants = BotConstants()
        self.query = self.update.callback_query
        self.chosen_option = self.query.data
        self.chat_id = self.query.message.chat_id
        self.message_id = self.query.message.message_id
        self.telegram_username = self.query.message.chat.username
        self.shadow_mode = ShadowMode(bot)
        self.iron_cache = IronCache()
        self.database_client = DatabaseClient()

    def get_strava_data(self):
        try:
            strava_data = ujson.loads(self.iron_cache.get(cache="stats", key=self.telegram_username).value)
        except:
            logging.warning("Failed to fetch from cache! Querying database..")
            strava_data = self.database_client.read_operation(
                self.bot_constants.QUERY_GET_STRAVA_DATA.format(telegram_username=self.telegram_username))[0]
            self.iron_cache.put(cache="stats", key=self.telegram_username, value=strava_data)

        return strava_data

    def stats_ride_button(self):
        message = self.bot_constants.MESSAGE_STATS_SUB_KEYBOARD_MENU
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   reply_markup=self.bot_constants.KEYBOARD_STATS_RIDE_KEYBOARD_MENU)

    def stats_ride_all_time_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.ride_stats("All Time Stats", "at")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_ride_ytd_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.ride_stats("Year to Date Stats", "ytd")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_ride_py_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.ride_stats("Previous Year Stats", "py")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_ride_cm_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.ride_stats("Current Month Stats", "cm")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_ride_pm_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.ride_stats("Previous Month Stats", "pm")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_run_button(self):
        message = self.bot_constants.MESSAGE_STATS_SUB_KEYBOARD_MENU
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   reply_markup=self.bot_constants.KEYBOARD_STATS_RUN_KEYBOARD_MENU)

    def stats_run_all_time_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.run_stats("All Time Stats", "at")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_run_ytd_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.run_stats("Year to Date Stats", "ytd")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_run_py_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.run_stats("Previous Year Stats", "py")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_run_cm_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.run_stats("Current Month Stats", "cm")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_run_pm_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.run_stats("Previous Month", "pm")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_swim_button(self):
        message = self.bot_constants.MESSAGE_STATS_SUB_KEYBOARD_MENU
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   reply_markup=self.bot_constants.KEYBOARD_STATS_SWIM_KEYBOARD_MENU)

    def stats_swim_all_time_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.swim_stats("All Time Stats", "at")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_swim_ytd_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.swim_stats("Year to Date Stats", "ytd")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_swim_py_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.swim_stats("Previous Year Stats", "py")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_swim_cm_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.swim_stats("Current Month Stats", "cm")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_swim_pm_button(self):
        format_stats = FormatStats(self.get_strava_data())
        message = format_stats.swim_stats("Previous Month Stats", "pm")
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.shadow_mode.send_message(message=message)
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.send_message(text=message, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def back_button(self):
        message = self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id,
                                   reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def exit_button(self):
        self.user_data.clear()
        message = self.bot_constants.MESSAGE_EXIT_BUTTON
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
        self.shadow_mode.send_message(message=message)

    def process(self):
        options = defaultdict(lambda: self.exit_button, {
            'stats_ride': self.stats_ride_button,
            'stats_ride_all_time': self.stats_ride_all_time_button,
            'stats_ride_ytd': self.stats_ride_ytd_button,
            'stats_ride_py': self.stats_ride_py_button,
            'stats_ride_cm': self.stats_ride_cm_button,
            'stats_ride_pm': self.stats_ride_pm_button,
            'stats_run': self.stats_run_button,
            'stats_run_all_time': self.stats_run_all_time_button,
            'stats_run_ytd': self.stats_run_ytd_button,
            'stats_run_py': self.stats_run_py_button,
            'stats_run_cm': self.stats_run_cm_button,
            'stats_run_pm': self.stats_run_pm_button,
            'stats_swim': self.stats_swim_button,
            'stats_swim_all_time': self.stats_swim_all_time_button,
            'stats_swim_ytd': self.stats_swim_ytd_button,
            'stats_swim_py': self.stats_swim_py_button,
            'stats_swim_cm': self.stats_swim_cm_button,
            'stats_swim_pm': self.stats_swim_pm_button,
            'stats_back': self.back_button,
            'stats_exit': self.exit_button
        })

        options[self.chosen_option]()
