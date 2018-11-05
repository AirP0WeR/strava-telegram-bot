#  -*- encoding: utf-8 -*-

import logging
import os
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import telegram
import psycopg2
from telegram.ext import Updater, CommandHandler

from scripts.common.aes_cipher import AESCipher
from scripts.commands.miscellaneous_stats import MiscellaneousStats
from scripts.commands.segments import Segments
from scripts.commands.stats import Stats
from scripts.commands.hundreds import Hundreds
from scripts.commands.fifties import Fifties


class EnvironmentalVariables(object):
    database_url = os.environ['DATABASE_URL']
    crypt_key_length = os.environ['CRYPT_KEY_LENGTH']
    crypt_key = os.environ['CRYPT_KEY']
    admin_user_name = os.environ['ADMIN_USER_NAME']
    app_name = os.environ.get('APP_NAME')
    port = os.environ.get('PORT')
    registration_url = os.environ['REGISTRATION_URL']
    shadow_mode = os.environ['SHADOW_MODE']
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']


class Bot(EnvironmentalVariables):
    QUERY_FETCH_TOKEN = "select access_token from athletes where telegram_username='{telegram_username}'"

    def __init__(self):
        self.aes_cipher = AESCipher(self.crypt_key_length, self.crypt_key)

    def send_messages(self, bot, update, messages):
        for message in messages:
            bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
            update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            if self.shadow_mode and (
                    int(self.aes_cipher.decrypt(os.environ['SHADOW_MODE_CHAT_ID'])) != int(update.message.chat_id)):
                bot.send_message(chat_id=self.aes_cipher.decrypt(os.environ['SHADOW_MODE_CHAT_ID']), text=message,
                                 parse_mode="Markdown", disable_notification=True,
                                 disable_web_page_preview=True)
            else:
                logging.info("Chat ID & Shadow Chat ID are the same")

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

    def handle_commands(self, bot, update, command):
        message = [
            "Hi {first_name}! You are not a registered user yet.\n\nVisit the following link to register: {registration_url}\n\nPing {admin_user_name} in case you face any issue.".format(
                first_name=update.message.from_user.first_name, registration_url=self.registration_url,
                admin_user_name=self.aes_cipher.decrypt(self.admin_user_name))]
        first_name = update.message.from_user.first_name
        athlete_token = self.get_athlete_token(bot, update)
        if athlete_token:

            if command == "start":
                message = ["Hey {first_name}! I'm your Strava Bot. " \
                           "Type '/' to get the list of commands that I understand.".format(first_name=first_name)]

            elif command == "stats":
                greeting = [
                    "Hey {first_name}! Give me a minute or two while I fetch your stats.".format(first_name=first_name)]
                self.send_messages(bot, update, greeting)
                message = Stats(athlete_token).main()

            elif command == "miscstats":
                greeting = ["Hey {first_name}! Give me a minute or two while I fetch your miscellaneous stats.".format(
                    first_name=first_name)]
                self.send_messages(bot, update, greeting)
                message = [MiscellaneousStats(athlete_token).main()]

            elif command == "segments":
                greeting = [
                    "Hey {first_name}! Give me a minute or two while I fetch your starred segments' stats.".format(
                        first_name=first_name)]
                self.send_messages(bot, update, greeting)
                message = Segments(athlete_token).main()

            elif command == "hundreds":
                greeting = ["Hey {first_name}! Give me a minute or two while I fetch your 100 km rides.".format(
                    first_name=first_name)]
                self.send_messages(bot, update, greeting)
                message = Hundreds(athlete_token).main()

            elif command == "fifties":
                greeting = ["Hey {first_name}! Give me a minute or two while I fetch your 50 km rides.".format(
                    first_name=first_name)]
                self.send_messages(bot, update, greeting)
                message = Fifties(athlete_token).main()

        self.send_messages(bot, update, message)

    def start(self, bot, update):
        self.handle_commands(bot, update, "start")

    def stats(self, bot, update):
        self.handle_commands(bot, update, "stats")

    def miscstats(self, bot, update):
        self.handle_commands(bot, update, "miscstats")

    def segments(self, bot, update):
        self.handle_commands(bot, update, "segments")

    def hundreds(self, bot, update):
        self.handle_commands(bot, update, "hundreds")

    def fifties(self, bot, update):
        self.handle_commands(bot, update, "fifties")

    @staticmethod
    def error(update, error):
        logging.error('Update "{update}" caused error "{error}"'.format(update=update, error=error))

    def main(self):

        updater = Updater(self.aes_cipher.decrypt(self.telegram_bot_token))
        dispatcher_handler = updater.dispatcher

        dispatcher_handler.add_handler(CommandHandler("start", self.start))
        dispatcher_handler.add_handler(CommandHandler("stats", self.stats))
        dispatcher_handler.add_handler(CommandHandler("miscstats", self.miscstats))
        dispatcher_handler.add_handler(CommandHandler("segments", self.segments))
        dispatcher_handler.add_handler(CommandHandler("100s", self.hundreds))
        dispatcher_handler.add_handler(CommandHandler("50s", self.fifties))

        dispatcher_handler.add_error_handler(self.error)

        updater.start_webhook(listen="0.0.0.0",
                              port=int(self.port),
                              url_path=self.aes_cipher.decrypt(self.telegram_bot_token))

        updater.bot.setWebhook("{app_name}/{telegram_bot_token}".format(app_name=self.app_name,
                                                                        telegram_bot_token=self.aes_cipher.decrypt(
                                                                            self.telegram_bot_token)))
        updater.idle()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    bot = Bot()
    bot.main()
