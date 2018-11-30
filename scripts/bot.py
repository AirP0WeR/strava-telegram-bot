#  -*- encoding: utf-8 -*-

import logging
import os
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import psycopg2
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from scripts.common.aes_cipher import AESCipher
from scripts.clients.strava import StravaClient
from scripts.stats.calculate_stats import CalculateStats
from scripts.stats.format_stats import FormatStats


class EnvironmentalVariables(object):
    database_url = os.environ['DATABASE_URL']
    crypt_key_length = os.environ['CRYPT_KEY_LENGTH']
    crypt_key = os.environ['CRYPT_KEY']
    admin_user_name = os.environ['ADMIN_USER_NAME']
    app_name = os.environ.get('APP_NAME')
    port = os.environ.get('PORT')
    registration_url = os.environ['REGISTRATION_URL']
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']


class Bot(EnvironmentalVariables):
    QUERY_FETCH_TOKEN = "select access_token from athletes where telegram_username='{telegram_username}'"

    STATS_MAIN_KEYBOARD_MENU = [[InlineKeyboardButton("Ride", callback_data='stats_ride'),
                                 InlineKeyboardButton("Run", callback_data='stats_run')],
                                [InlineKeyboardButton("Exit", callback_data='exit')]]

    STATS_RIDE_KEYBOARD_MENU = [[InlineKeyboardButton("All Time", callback_data='stats_ride_all_time'),
                                 InlineKeyboardButton("Year to Date", callback_data='stats_ride_ytd')],
                                [InlineKeyboardButton("Exit", callback_data='exit')]]

    STATS_RUN_KEYBOARD_MENU = [[InlineKeyboardButton("All Time", callback_data='stats_run_all_time'),
                                InlineKeyboardButton("Year to Date", callback_data='stats_run_ytd')],
                               [InlineKeyboardButton("Exit", callback_data='exit')]]

    def __init__(self):
        self.aes_cipher = AESCipher(self.crypt_key_length, self.crypt_key)

    def get_athlete_token(self, bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        username = update.message.from_user.username
        database_connection = psycopg2.connect(self.database_url, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(self.QUERY_FETCH_TOKEN.format(telegram_username=username))
        result = cursor.fetchone()
        cursor.close()
        database_connection.close()
        if result:
            return self.aes_cipher.decrypt(result[0])
        else:
            return False

    @staticmethod
    def start(bot, update):
        message = "Hey {first_name}! I'm your Strava Bot. Type '/' to get the list of commands that I understand.".format(
            first_name=update.message.from_user.first_name)
        update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

    def stats(self, bot, update, user_data):
        athlete_token = self.get_athlete_token(bot, update)
        if athlete_token:
            greeting = "Hey {first_name}! Give me a minute or two while I fetch your data.".format(
                first_name=update.message.from_user.first_name)
            update.message.reply_text(greeting, parse_mode="Markdown", disable_web_page_preview=True)

            strava_client = StravaClient(athlete_token).get_strava_client()
            activities = strava_client.get_activities()

            calculated_stats = CalculateStats(activities).main()
            formatted_stats = FormatStats(calculated_stats).main()
            user_data['stats'] = formatted_stats

            update.message.reply_text('Choose an Activity to view your stats:',
                                      reply_markup=InlineKeyboardMarkup(self.STATS_MAIN_KEYBOARD_MENU))
        else:
            message = "Hi {first_name}! You are not a registered user yet.\n\nVisit the following link to register: {registration_url}\n\nPing {admin_user_name} in case you face any issue.".format(
                first_name=update.message.from_user.first_name, registration_url=self.registration_url,
                admin_user_name=self.aes_cipher.decrypt(self.admin_user_name))
            update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

    def button(self, bot, update, user_data):
        query = update.callback_query
        chosen_option = query.data
        chat_id = query.message.chat_id
        message_id = query.message.message_id
        stats_ride_all_time = user_data['stats']['all_time_ride_stats']
        stats_ride_ytd = user_data['stats']['ytd_ride_stats']
        stats_run_all_time = user_data['stats']['all_time_run_stats']
        stats_run_ytd = user_data['stats']['ytd_run_stats']

        if chosen_option == "stats_ride":
            bot.edit_message_text(text="Choose the type of stat you want to see:",
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  reply_markup=InlineKeyboardMarkup(self.STATS_RIDE_KEYBOARD_MENU))

        elif chosen_option == "stats_ride_all_time":
            bot.edit_message_text(text=stats_ride_all_time,
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  parse_mode="Markdown",
                                  disable_web_page_preview=True)

            bot.send_message(text="Choose an Activity to view your stats:",
                             chat_id=chat_id,
                             reply_markup=InlineKeyboardMarkup(self.STATS_MAIN_KEYBOARD_MENU))

        elif chosen_option == "stats_ride_ytd":
            bot.edit_message_text(text=stats_ride_ytd,
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  parse_mode="Markdown",
                                  disable_web_page_preview=True)

            bot.send_message(text="Choose an Activity to view your stats:",
                             chat_id=chat_id,
                             reply_markup=InlineKeyboardMarkup(self.STATS_MAIN_KEYBOARD_MENU))

        elif chosen_option == "stats_run":
            bot.edit_message_text(text="Choose the type of stat you want to see:",
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  reply_markup=InlineKeyboardMarkup(self.STATS_RUN_KEYBOARD_MENU))

        elif chosen_option == "stats_run_all_time":
            bot.edit_message_text(text=stats_run_all_time,
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  parse_mode="Markdown",
                                  disable_web_page_preview=True)

            bot.send_message(text="Choose an Activity to view your stats:",
                             chat_id=chat_id,
                             reply_markup=InlineKeyboardMarkup(self.STATS_MAIN_KEYBOARD_MENU))

        elif chosen_option == "stats_run_ytd":
            bot.edit_message_text(text=stats_run_ytd,
                                  chat_id=chat_id,
                                  message_id=message_id,
                                  parse_mode="Markdown",
                                  disable_web_page_preview=True)

            bot.send_message(text="Choose an Activity to view your stats:",
                             chat_id=chat_id,
                             reply_markup=InlineKeyboardMarkup(self.STATS_MAIN_KEYBOARD_MENU))

        elif chosen_option == "exit":
            user_data.clear()
            bot.edit_message_text(text="Thank you!", chat_id=chat_id, message_id=message_id)

    @staticmethod
    def error(update, error):
        logger.error('Update "{update}" caused error "{error}"'.format(update=update, error=error))

    def main(self):

        updater = Updater(self.aes_cipher.decrypt(self.telegram_bot_token))
        dispatcher_handler = updater.dispatcher

        dispatcher_handler.add_handler(CommandHandler("start", self.start))
        dispatcher_handler.add_handler(CommandHandler("stats", self.stats, pass_user_data=True))
        dispatcher_handler.add_handler((CallbackQueryHandler(self.button, pass_user_data=True)))

        dispatcher_handler.add_error_handler(self.error)

        updater.start_webhook(listen="0.0.0.0", port=int(self.port),
                              url_path=self.aes_cipher.decrypt(self.telegram_bot_token))

        updater.bot.setWebhook("{app_name}/{telegram_bot_token}".format(app_name=self.app_name,
                                                                        telegram_bot_token=self.aes_cipher.decrypt(
                                                                            self.telegram_bot_token)))
        updater.idle()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    strava_bot = Bot()
    strava_bot.main()
