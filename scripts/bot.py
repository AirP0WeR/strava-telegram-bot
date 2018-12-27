#  -*- encoding: utf-8 -*-

import logging
from os import sys, path

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.aes_cipher import AESCipher
from scripts.handle.buttons import HandleButtons
from scripts.common.constants_and_variables import BotVariables
from scripts.handle.commands import HandleCommands


class StravaTelegramBot(object):

    def __init__(self):
        self.bot_variables = BotVariables()
        self.aes_cipher = AESCipher(self.bot_variables.crypt_key_length, self.bot_variables.crypt_key)

    @staticmethod
    def error(update, error):
        logger.error('Update "{update}" caused error "{error}"'.format(update=update, error=error))

    @staticmethod
    def handle_commands(bot, update, user_data):
        commands = HandleCommands(bot, update, user_data)
        commands.process()

    @staticmethod
    def handle_buttons(bot, update, user_data):
        buttons = HandleButtons(bot, update, user_data)
        buttons.process()

    def main(self):
        updater = Updater(self.aes_cipher.decrypt(self.bot_variables.telegram_bot_token))
        dispatcher_handler = updater.dispatcher

        dispatcher_handler.add_handler(CommandHandler("start", self.handle_commands, pass_user_data=True))
        dispatcher_handler.add_handler(CommandHandler("stats", self.handle_commands, pass_user_data=True))
        dispatcher_handler.add_handler(CallbackQueryHandler(self.handle_buttons, pass_user_data=True))

        dispatcher_handler.add_error_handler(self.error)

        updater.start_webhook(listen="0.0.0.0", port=self.bot_variables.port,
                              url_path=self.aes_cipher.decrypt(self.bot_variables.telegram_bot_token))

        updater.bot.setWebhook("{app_name}/{telegram_bot_token}".format(app_name=self.bot_variables.app_name,
                                                                        telegram_bot_token=self.aes_cipher.decrypt(
                                                                            self.bot_variables.telegram_bot_token)))
        updater.idle()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    strava_telegram_bot = StravaTelegramBot()
    strava_telegram_bot.main()
