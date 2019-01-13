#  -*- encoding: utf-8 -*-

from collections import defaultdict
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.constants_and_variables import BotConstants


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
        self.all_time_ride_stats = self.user_data['stats']['all_time_ride_stats']
        self.ytd_ride_stats = self.user_data['stats']['ytd_ride_stats']
        self.py_ride_stats = self.user_data['stats']['py_ride_stats']
        self.cm_ride_stats = self.user_data['stats']['cm_ride_stats']
        self.pm_ride_stats = self.user_data['stats']['pm_ride_stats']
        self.all_time_run_stats = self.user_data['stats']['all_time_run_stats']
        self.ytd_run_stats = self.user_data['stats']['ytd_run_stats']
        self.py_run_stats = self.user_data['stats']['py_run_stats']
        self.cm_run_stats = self.user_data['stats']['cm_run_stats']
        self.pm_run_stats = self.user_data['stats']['pm_run_stats']

    def stats_ride_button(self):
        self.bot.edit_message_text(text=self.bot_constants.MESSAGE_STATS_RIDE_KEYBOARD_MENU, chat_id=self.chat_id,
                                   message_id=self.message_id,
                                   reply_markup=self.bot_constants.KEYBOARD_STATS_RIDE_KEYBOARD_MENU)

    def stats_ride_all_time_button(self):
        self.bot.edit_message_text(text=self.all_time_ride_stats, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_ride_ytd_button(self):
        self.bot.edit_message_text(text=self.ytd_ride_stats, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_ride_py_button(self):
        self.bot.edit_message_text(text=self.py_ride_stats, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_ride_cm_button(self):
        self.bot.edit_message_text(text=self.cm_ride_stats, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_ride_pm_button(self):
        self.bot.edit_message_text(text=self.pm_ride_stats, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_run_button(self):
        self.bot.edit_message_text(text=self.bot_constants.MESSAGE_STATS_RIDE_KEYBOARD_MENU, chat_id=self.chat_id,
                                   message_id=self.message_id,
                                   reply_markup=self.bot_constants.KEYBOARD_STATS_RUN_KEYBOARD_MENU)

    def stats_run_all_time_button(self):
        self.bot.edit_message_text(text=self.all_time_run_stats, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_run_ytd_button(self):
        self.bot.edit_message_text(text=self.ytd_run_stats, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)

        self.bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_run_py_button(self):
        self.bot.edit_message_text(text=self.py_run_stats, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_run_cm_button(self):
        self.bot.edit_message_text(text=self.cm_run_stats, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def stats_run_pm_button(self):
        self.bot.edit_message_text(text=self.pm_run_stats, chat_id=self.chat_id, message_id=self.message_id,
                                   parse_mode="Markdown", disable_web_page_preview=True)
        self.bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU, chat_id=self.chat_id,
                              reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def back_button(self):
        self.bot.edit_message_text(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU, chat_id=self.chat_id,
                                   message_id=self.message_id,
                                   reply_markup=self.bot_constants.KEYBOARD_STATS_MAIN_KEYBOARD_MENU)

    def exit_button(self):
        self.user_data.clear()
        self.bot.edit_message_text(text=self.bot_constants.MESSAGE_EXIT_BUTTON, chat_id=self.chat_id,
                                   message_id=self.message_id)

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
            'stats_back': self.back_button,
            'stats_exit': self.exit_button
        })

        options[self.chosen_option]()
