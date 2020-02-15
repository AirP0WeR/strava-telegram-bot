#  -*- encoding: utf-8 -*-

import logging
import traceback

import facebook
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, CallbackContext, MessageHandler

from common.constants_and_variables import BotVariables
from handle.buttons import HandleButtons
from handle.command_args import HandleCommandArgs
from handle.commands import HandleCommands
from resources.strava_telegram_webhooks import StravaTelegramWebhooksResource


class StravaTelegramBot:
    RIDERS = {
        "12001": "Balakrishna Udyavara",
        "12640": "Jnanashekar U P",
        "4904": "Naveen Solanki",
        "5243": "Narayana Badri",
        "13294": "Sheethal Kumar Gurusiddappa",
        "10792": "Supreeth Gopalakrishna Vattam",
        "13697": "Santhosh Kumar M S",
        "13696": "Dhanaprakash M S",
        "13226": "Kikkeri Puttegowda Jayaramu",
        "11932": "Sumit Gehani",
        "12256": "Sowmya Chandran",
        "10469": "Parameshwar Hegde",
        "8608": "Madhu Krishna Iyengar",
        "10274": "G Ravi Kumar",
        "8361": "Kishore Kumar"
    }

    def __init__(self):
        self.bot_variables = BotVariables()
        self.strava_telegram_webhooks_resource = StravaTelegramWebhooksResource()

    @staticmethod
    def error(update, context):
        logger.error('Update %s caused error %s', update, context.error)

    def handle_commands(self, update: Update, context: CallbackContext):
        try:
            commands = HandleCommands(context.bot, update, context.user_data)
            commands.process()
        except Exception:
            message = "Something went wrong. Exception: {exception}".format(exception=traceback.format_exc())
            logging.error(message)
            self.strava_telegram_webhooks_resource.send_message(message)

    def handle_buttons(self, update: Update, context: CallbackContext):
        try:
            buttons = HandleButtons(context.bot, update, context.user_data)
            buttons.process()
        except Exception:
            message = "Something went wrong. Exception: {exception}".format(exception=traceback.format_exc())
            logging.error(message)
            self.strava_telegram_webhooks_resource.send_message(message)

    def handle_command_args(self, update: Update, context: CallbackContext):
        try:
            if len(context.args) > 0:
                command_args = HandleCommandArgs(context.bot, update, context.args)
                command_args.process()
            else:
                logging.warning("No arguments passed.")
        except Exception:
            message = "Something went wrong. Exception: {exception}".format(exception=traceback.format_exc())
            logging.error(message)
            self.strava_telegram_webhooks_resource.send_message(message)

    def image_handler(self, update: Update, context: CallbackContext):
        logging.info("Received post finish post on Facebook: {}".format(update.message.caption))
        caption_split = update.message.caption.split()
        if len(caption_split) == 2:
            rider_no = caption_split[0]
            finish_time = caption_split[1]
            rider_name = self.RIDERS[rider_no]
            caption = "{rider_name} finished at {finish_time}\n\n.\n.\n#AudaxMysuru #AudaxIndia #Cycling #Brevet #Randonneuring #HighwayExpress300".format(
                rider_name=rider_name, finish_time=finish_time)
            rider_photo = context.bot.get_file(update.message.photo[-1])
            rider_photo.download("/tmp/rider_photo.jpg")
            graph = facebook.GraphAPI(access_token=self.bot_variables.facebook_token)
            graph.put_photo(image=open('/tmp/rider_photo.jpg', 'rb'), album_path='110287720378697/photos',
                            caption=caption)
            message = "Uploaded finish post for {}: {}".format(rider_no, rider_name)
            logging.info(message)
            self.strava_telegram_webhooks_resource.send_message(message)

    def main(self):
        updater = Updater(self.bot_variables.telegram_bot_token, use_context=True, workers=16)
        dispatcher_handler = updater.dispatcher

        dispatcher_handler.add_handler(CommandHandler("start", self.handle_commands, pass_user_data=True))
        dispatcher_handler.add_handler(CommandHandler("next", self.handle_commands, pass_user_data=True))
        dispatcher_handler.add_handler(CommandHandler("stats", self.handle_commands, pass_user_data=True))
        dispatcher_handler.add_handler(CommandHandler("refresh_stats", self.handle_commands, pass_user_data=True))
        dispatcher_handler.add_handler(
            CommandHandler("challenges_refresh_stats", self.handle_command_args, pass_args=True))
        dispatcher_handler.add_handler(
            CommandHandler("challenges_deauth", self.handle_command_args, pass_args=True))
        dispatcher_handler.add_handler(
            CommandHandler("challenges_refresh_all_stats", self.handle_commands, pass_user_data=True,
                           filters=Filters.user(username=self.bot_variables.admins)))
        dispatcher_handler.add_handler(
            CommandHandler("auto_update_indoor_ride", self.handle_commands, pass_user_data=True))
        dispatcher_handler.add_handler(CommandHandler("cancel", self.handle_commands, pass_user_data=True))
        dispatcher_handler.add_handler(CommandHandler("all_athletes", self.handle_commands, pass_user_data=True,
                                                      filters=Filters.user(username=self.bot_variables.admins)))
        dispatcher_handler.add_handler(
            CommandHandler("challenges_even_athletes", self.handle_commands, pass_user_data=True,
                           filters=Filters.user(username=self.bot_variables.admins)))
        dispatcher_handler.add_handler(
            CommandHandler("challenges_odd_athletes", self.handle_commands, pass_user_data=True,
                           filters=Filters.user(username=self.bot_variables.admins)))
        dispatcher_handler.add_handler(
            CommandHandler("challenges_hits_reset", self.handle_commands, pass_user_data=True,
                           filters=Filters.user(username=self.bot_variables.admins)))
        dispatcher_handler.add_handler(
            CommandHandler("refresh_all_stats", self.handle_commands, pass_user_data=True,
                           filters=Filters.user(username=self.bot_variables.admins)))
        dispatcher_handler.add_handler(CommandHandler("activity_summary", self.handle_commands, pass_user_data=True))
        dispatcher_handler.add_handler(CommandHandler("help", self.handle_commands, pass_user_data=True))
        dispatcher_handler.add_handler(CommandHandler("token", self.handle_command_args, pass_args=True,
                                                      filters=Filters.user(username=self.bot_variables.admins)))
        dispatcher_handler.add_handler(CommandHandler("activate", self.handle_command_args, pass_args=True,
                                                      filters=Filters.user(username=self.bot_variables.admins)))
        dispatcher_handler.add_handler(CommandHandler("deactivate", self.handle_command_args, pass_args=True,
                                                      filters=Filters.user(username=self.bot_variables.admins)))
        dispatcher_handler.add_handler(CommandHandler("update", self.handle_command_args, pass_args=True,
                                                      filters=Filters.user(username=self.bot_variables.admins)))
        updater.dispatcher.add_handler(MessageHandler(Filters.photo, self.image_handler))
        dispatcher_handler.add_handler(CallbackQueryHandler(self.handle_buttons, pass_user_data=True))

        dispatcher_handler.add_error_handler(self.error)

        updater.start_webhook(listen="0.0.0.0", port=self.bot_variables.port,
                              url_path=self.bot_variables.telegram_bot_token)

        updater.bot.setWebhook("{app_name}/{telegram_bot_token}".format(app_name=self.bot_variables.app_name,
                                                                        telegram_bot_token=self.bot_variables.telegram_bot_token))
        updater.idle()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.os.environ.get('LOGGING_LEVEL'))
    logger = logging.getLogger(__name__)
    strava_telegram_bot = StravaTelegramBot()
    strava_telegram_bot.main()
