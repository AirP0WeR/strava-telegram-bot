#  -*- encoding: utf-8 -*-

import logging
import traceback

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters

from scripts.common.constants_and_variables import BotVariables
from scripts.common.shadow_mode import ShadowMode
from scripts.handle.buttons import HandleButtons
from scripts.handle.commands import HandleCommands


class StravaTelegramBot(object):

    def __init__(self):
        self.bot_variables = BotVariables()
        self.shadow_mode = ShadowMode()

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
        try:
            updater = Updater(self.bot_variables.telegram_bot_token)
            dispatcher_handler = updater.dispatcher

            dispatcher_handler.add_handler(CommandHandler("start", self.handle_commands, pass_user_data=True))
            dispatcher_handler.add_handler(CommandHandler("stats", self.handle_commands, pass_user_data=True))
            dispatcher_handler.add_handler(CommandHandler("refresh_stats", self.handle_commands, pass_user_data=True))
            dispatcher_handler.add_handler(
                CommandHandler("auto_update_indoor_ride", self.handle_commands, pass_user_data=True))
            dispatcher_handler.add_handler(CommandHandler("cancel", self.handle_commands, pass_user_data=True))
            dispatcher_handler.add_handler(CommandHandler("all_athletes", self.handle_commands, pass_user_data=True,
                                                          filters=Filters.user(username=self.bot_variables.admins)))
            dispatcher_handler.add_handler(
                CommandHandler("refresh_all_stats", self.handle_commands, pass_user_data=True,
                               filters=Filters.user(username=self.bot_variables.admins)))
            dispatcher_handler.add_handler(CallbackQueryHandler(self.handle_buttons, pass_user_data=True))

            dispatcher_handler.add_error_handler(self.error)

            updater.start_webhook(listen="0.0.0.0", port=self.bot_variables.port,
                                  url_path=self.bot_variables.telegram_bot_token)

            updater.bot.setWebhook("{app_name}/{telegram_bot_token}".format(app_name=self.bot_variables.app_name,
                                                                            telegram_bot_token=self.bot_variables.telegram_bot_token))
            updater.idle()

        except Exception:
            message = "Something went wrong. Exception: {exception}".format(exception=traceback.format_exc())
            logging.error(message)
            self.shadow_mode.send_message(message)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.os.environ.get('LOGGING_LEVEL'))
    logger = logging.getLogger(__name__)
    strava_telegram_bot = StravaTelegramBot()
    strava_telegram_bot.main()
