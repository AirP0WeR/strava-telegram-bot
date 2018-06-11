#!/usr/bin/env python
import logging
import os
import sys
from threading import Thread

import telegram
from telegram.ext import Updater, CommandHandler, Filters

from aes_cipher import AESCipher
from config import Config
from miscellaneous_stats import MiscellaneousStats
from segments import Segments
from stats import Stats


class Bot(object):

    def __init__(self):
        logging.info("Initializing %s" % self.__class__.__name__)

    @staticmethod
    def send_message(bot, update, message):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
        if config['SHADOW_MODE'] and (
                int(aes_cipher.decrypt(config['SHADOW_MODE_CHAT_ID'])) != int(update.message.chat_id)):
            bot.send_message(chat_id=aes_cipher.decrypt(config['SHADOW_MODE_CHAT_ID']), text=message,
                             parse_mode="Markdown", disable_notification=True,
                             disable_web_page_preview=True)
        else:
            logging.info("Chat ID & Shadow Chat ID are the same")

    @staticmethod
    def get_athlete_token(bot, update):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        username = update.message.from_user.username
        if username in config['ATHLETES'].viewkeys():
            return {"Authorization": "Bearer " + aes_cipher.decrypt(config['ATHLETES'][username])}
        else:
            return False

    def handle_commands(self, bot, update, command):
        message = "Hi %s! You are not a registered user yet. Contact %s for more details." \
                  % (update.message.from_user.first_name, aes_cipher.decrypt(config['ADMIN_USER_NAME']))
        athlete_token = self.get_athlete_token(bot, update)
        if athlete_token:

            if command == "start":
                message = "Hey %s! I'm your Strava Bot. " \
                          "Type '/' to get the list of commands that I understand." \
                          % update.message.from_user.first_name

            elif command == "stats":
                greeting = "Hey %s! Give me a few moments while I give your stats." \
                           % update.message.from_user.first_name
                self.send_message(bot, update, greeting)
                message = Stats(athlete_token, command).main()

            elif command == "miscstats":
                greeting = "Hey %s! Give me a few moments while I give some Miscellaneous stats." \
                           % update.message.from_user.first_name
                self.send_message(bot, update, greeting)
                message = MiscellaneousStats(athlete_token).main()

            elif command == "segments":
                greeting = "Hey %s! Give me a few moments while I give your Starred Segments' stats." \
                           % update.message.from_user.first_name
                self.send_message(bot, update, greeting)
                message = Segments(bot, update, athlete_token, config['SHADOW_MODE'],
                                   aes_cipher.decrypt(config['SHADOW_MODE_CHAT_ID'])).main()

        self.send_message(bot, update, message)

    def start(self, bot, update):
        self.handle_commands(bot, update, "start")

    def stats(self, bot, update):
        self.handle_commands(bot, update, "stats")

    def miscstats(self, bot, update):
        self.handle_commands(bot, update, "miscstats")

    def segments(self, bot, update):
        self.handle_commands(bot, update, "segments")

    @staticmethod
    def error(update, error):
        logger.warning('Update "%s" caused error "%s"', update, error)

    def main(self):

        def stop_and_restart():
            updater.stop()
            os.execl(sys.executable, sys.executable, *sys.argv)

        def restart(bot, update):
            self.send_message(bot, update, "Bot is restarting...")
            Thread(target=stop_and_restart).start()

        updater = Updater(aes_cipher.decrypt(os.environ['TELEGRAM_BOT_TOKEN']))
        dispatcher_handler = updater.dispatcher

        dispatcher_handler.add_handler(CommandHandler("start", self.start))
        dispatcher_handler.add_handler(CommandHandler("stats", self.stats))
        dispatcher_handler.add_handler(CommandHandler("miscstats", self.miscstats))
        dispatcher_handler.add_handler(CommandHandler("segments", self.segments))
        dispatcher_handler.add_handler(
            CommandHandler('restart', restart,
                           filters=Filters.user(username=aes_cipher.decrypt(config['ADMIN_USER_NAME']))))

        dispatcher_handler.add_error_handler(self.error)

        updater.start_webhook(listen="0.0.0.0",
                              port=int(os.environ.get('PORT')),
                              url_path=aes_cipher.decrypt(os.environ['TELEGRAM_BOT_TOKEN']))

        updater.bot.setWebhook("{}/{}".format(os.environ.get('APP_NAME'), aes_cipher.decrypt(
            os.environ['TELEGRAM_BOT_TOKEN'])))
        updater.idle()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    aes_cipher = AESCipher(os.environ['CRYPT_KEY_LENGTH'], os.environ['CRYPT_KEY'])
    config = Config().main()
    Bot().main()
