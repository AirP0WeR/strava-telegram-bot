#  -*- encoding: utf-8 -*-

import logging
import os
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from threading import Thread

import telegram
import psycopg2
from telegram.ext import Updater, CommandHandler, Filters

from scripts.common.aes_cipher import AESCipher
from scripts.commands.miscellaneous_stats import MiscellaneousStats
from scripts.commands.segments import Segments
from scripts.commands.stats import Stats
from scripts.commands.hundreds import Hundreds
from scripts.commands.fifties import Fifties

class Bot(object):
    DATABASE_URL = os.environ['DATABASE_URL']
    QUERY_FETCH_TOKEN = "select access_token from athletes where telegram_username='{}'"

    def __init__(self):
        logging.info("Initializing %s" % self.__class__.__name__)

    @staticmethod
    def send_messages(bot, update, messages):
        for message in messages:
            bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
            update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            if os.environ['SHADOW_MODE'] and (
                    int(aes_cipher.decrypt(os.environ['SHADOW_MODE_CHAT_ID'])) != int(update.message.chat_id)):
                bot.send_message(chat_id=aes_cipher.decrypt(os.environ['SHADOW_MODE_CHAT_ID']), text=message,
                                 parse_mode="Markdown", disable_notification=True,
                                 disable_web_page_preview=True)
            else:
                logging.info("Chat ID & Shadow Chat ID are the same")

    def get_athlete_token(self, bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        username = update.message.from_user.username
        database_connection = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = database_connection.cursor()
        cursor.execute(self.QUERY_FETCH_TOKEN.format(username))
        result = cursor.fetchone()
        database_connection.close()
        if result:
            return aes_cipher.decrypt(result[0])
        else:
            return False

    def handle_commands(self, bot, update, command):
        message = [
            "Hi {}! You are not a registered user yet.\n\nVisit the following link to register: {}\n\nPing {} in case you face any issue.".format(
            update.message.from_user.first_name, os.environ['REGISTRATION_URL'],
                aes_cipher.decrypt(os.environ['ADMIN_USER_NAME']))]
        athlete_token = self.get_athlete_token(bot, update)
        if athlete_token:

            if command == "start":
                message = ["Hey %s! I'm your Strava Bot. " \
                           "Type '/' to get the list of commands that I understand." \
                           % update.message.from_user.first_name]

            elif command == "stats":
                greeting = ["Hey %s! Give me a minute or two while I fetch your stats." \
                            % update.message.from_user.first_name]
                self.send_messages(bot, update, greeting)
                message = [Stats(athlete_token, command).main()]

            elif command == "miscstats":
                greeting = ["Hey %s! Give me a minute or two while I fetch your miscellaneous stats." \
                            % update.message.from_user.first_name]
                self.send_messages(bot, update, greeting)
                message = [MiscellaneousStats(athlete_token).main()]

            elif command == "segments":
                greeting = ["Hey %s! Give me a minute or two while I fetch your starred segments' stats." \
                            % update.message.from_user.first_name]
                self.send_messages(bot, update, greeting)
                message = Segments(athlete_token).main()

            elif command == "hundreds":
                greeting = ["Hey %s! Give me a minute or two while I fetch your 100 km rides." \
                            % update.message.from_user.first_name]
                self.send_messages(bot, update, greeting)
                message = Hundreds(athlete_token).main()

            elif command == "fifties":
                greeting = ["Hey %s! Give me a minute or two while I fetch your 50 km rides." \
                            % update.message.from_user.first_name]
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
        logger.warning('Update "%s" caused error "%s"', update, error)

    def main(self):

        def stop_and_restart():
            updater.stop()
            os.execl(sys.executable, sys.executable, *sys.argv)

        def restart(bot, update):
            self.send_messages(bot, update, ["Bot is restarting..."])
            Thread(target=stop_and_restart).start()

        updater = Updater(aes_cipher.decrypt(os.environ['TELEGRAM_BOT_TOKEN']))
        dispatcher_handler = updater.dispatcher

        dispatcher_handler.add_handler(CommandHandler("start", self.start))
        dispatcher_handler.add_handler(CommandHandler("stats", self.stats))
        dispatcher_handler.add_handler(CommandHandler("miscstats", self.miscstats))
        dispatcher_handler.add_handler(CommandHandler("segments", self.segments))
        dispatcher_handler.add_handler(CommandHandler("100s", self.hundreds))
        dispatcher_handler.add_handler(CommandHandler("50s", self.fifties))
        dispatcher_handler.add_handler(
            CommandHandler('restart', restart,
                           filters=Filters.user(username=aes_cipher.decrypt(os.environ['ADMIN_USER_NAME']))))

        dispatcher_handler.add_error_handler(self.error)

        updater.start_webhook(listen="0.0.0.0",
                              port=int(os.environ.get('PORT')),
                              url_path=aes_cipher.decrypt(os.environ['TELEGRAM_BOT_TOKEN']))

        updater.bot.setWebhook("{}/{}".format(os.environ.get('APP_NAME'), aes_cipher.decrypt(
            os.environ['TELEGRAM_BOT_TOKEN'])))
        updater.idle()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    aes_cipher = AESCipher(os.environ['CRYPT_KEY_LENGTH'], os.environ['CRYPT_KEY'])
    Bot().main()
