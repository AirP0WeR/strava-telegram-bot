#!/usr/bin/env python
import logging
import os
import sys
from threading import Thread

import telegram
from telegram.ext import Updater, CommandHandler, Filters

from resources.fun_stats import FunStats
from resources.stats import Stats
from resources.update_activity import UpdateActivity
from scripts.utils import AESCipher
from utils.config import Config


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
                greeting = "Hey %s! Give me a moment or two while I give your stats." \
                           % update.message.from_user.first_name
                self.send_message(bot, update, greeting)
                message = Stats(bot, update, athlete_token, command).main()

            elif command == "funstats":
                greeting = "Hey %s! Give me a moment or two while I give some of your fun stats." \
                           % update.message.from_user.first_name
                self.send_message(bot, update, greeting)
                message = FunStats(bot, update, athlete_token).main()

            elif command == "updatetowalk":
                greeting = "Hey %s! Give me a moment while I update your latest activity to Walk." \
                           % update.message.from_user.first_name
                self.send_message(bot, update, greeting)
                message = UpdateActivity(bot, update, "Walk", athlete_token).main()

        self.send_message(bot, update, message)

    def start(self, bot, update):
        self.handle_commands(bot, update, "start")

    def stats(self, bot, update):
        self.handle_commands(bot, update, "stats")

    def funstats(self, bot, update):
        self.handle_commands(bot, update, "funstats")

    def updatetowalk(self, bot, update):
        self.handle_commands(bot, update, "updatetowalk")

    @staticmethod
    def error(update, error):
        logger.warning('Update "%s" caused error "%s"', update, error)

    def main(self):
        telegram_token = config['PROD_TELEGRAM_BOT_TOKEN'] if config['ENVIRONMENT'] == "PROD" else config[
            'DEV_TELEGRAM_BOT_TOKEN']
        updater = Updater(aes_cipher.decrypt(telegram_token))
        dispatcher_handler = updater.dispatcher

        def stop_and_restart():
            updater.stop()
            os.execl(sys.executable, sys.executable, *sys.argv)

        def restart(bot, update):
            self.send_message(bot, update, "Bot is restarting...")
            Thread(target=stop_and_restart).start()

        dispatcher_handler.add_handler(CommandHandler("start", self.start))
        dispatcher_handler.add_handler(CommandHandler("stats", self.stats))
        dispatcher_handler.add_handler(CommandHandler("funstats", self.funstats))
        dispatcher_handler.add_handler(CommandHandler("updatetowalk", self.updatetowalk))
        dispatcher_handler.add_handler(
            CommandHandler('restart', restart,
                           filters=Filters.user(username=aes_cipher.decrypt(config['ADMIN_USER_NAME']))))

        dispatcher_handler.add_error_handler(self.error)
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    config = Config().main()
    aes_cipher = AESCipher(config['CRYPT_KEY_LENGTH'], config['CRYPT_KEY'])
    Bot().main()
