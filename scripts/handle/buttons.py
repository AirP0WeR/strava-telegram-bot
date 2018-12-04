#  -*- encoding: utf-8 -*-

from os import sys, path

from telegram import InlineKeyboardMarkup

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.constants_and_variables import BotConstants


class HandleButtons(object):

    def __init__(self):
        self.bot_constants = BotConstants()

    def button(self, bot, update, user_data):
        query = update.callback_query
        chosen_option = query.data
        chat_id = query.message.chat_id
        message_id = query.message.message_id
        stats_ride_all_time = user_data['stats']['all_time_ride_stats']
        stats_ride_ytd = user_data['stats']['ytd_ride_stats']
        stats_run_all_time = user_data['stats']['all_time_run_stats']
        stats_run_ytd = user_data['stats']['ytd_run_stats']
        stats_ride_misc = user_data['stats']['misc_ride_stats']

        if chosen_option == "stats_ride":
            bot.edit_message_text(text=self.bot_constants.MESSAGE_STATS_RIDE_KEYBOARD_MENU,
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_RIDE_KEYBOARD_MENU))

        elif chosen_option == "stats_ride_all_time":
            bot.edit_message_text(text=stats_ride_all_time,
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  parse_mode="Markdown",
                                  disable_web_page_preview=True)

            bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU,
                             chat_id=chat_id,
                             reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_MAIN_KEYBOARD_MENU))

        elif chosen_option == "stats_ride_ytd":
            bot.edit_message_text(text=stats_ride_ytd,
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  parse_mode="Markdown",
                                  disable_web_page_preview=True)

            bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU,
                             chat_id=chat_id,
                             reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_MAIN_KEYBOARD_MENU))

        elif chosen_option == "stats_ride_misc":
            bot.edit_message_text(text=stats_ride_misc,
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  parse_mode="Markdown",
                                  disable_web_page_preview=True)

            bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU,
                             chat_id=chat_id,
                             reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_MAIN_KEYBOARD_MENU))

        elif chosen_option == "stats_run":
            bot.edit_message_text(text=self.bot_constants.MESSAGE_STATS_RIDE_KEYBOARD_MENU,
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_RUN_KEYBOARD_MENU))

        elif chosen_option == "stats_run_all_time":
            bot.edit_message_text(text=stats_run_all_time,
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  parse_mode="Markdown",
                                  disable_web_page_preview=True)

            bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU,
                             chat_id=chat_id,
                             reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_MAIN_KEYBOARD_MENU))

        elif chosen_option == "stats_run_ytd":
            bot.edit_message_text(text=stats_run_ytd,
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  parse_mode="Markdown",
                                  disable_web_page_preview=True)

            bot.send_message(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU,
                             chat_id=chat_id,
                             reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_MAIN_KEYBOARD_MENU))

        elif chosen_option == "back":
            bot.edit_message_text(text=self.bot_constants.MESSAGE_STATS_MAIN_KEYBOARD_MENU,
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  reply_markup=InlineKeyboardMarkup(self.bot_constants.STATS_MAIN_KEYBOARD_MENU))

        elif chosen_option == "exit":
            user_data.clear()
            bot.edit_message_text(text=self.bot_constants.MESSAGE_EXIT_BUTTON, chat_id=chat_id, message_id=message_id)
