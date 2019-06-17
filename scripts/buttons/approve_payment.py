#  -*- encoding: utf-8 -*-
import logging

from common.constants_and_variables import BotConstants, BotVariables
from resources.strava_telegram_webhooks import StravaTelegramWebhooksResource


class ApprovePayment:

    def __init__(self, bot, update, user_data):
        self.bot = bot
        self.update = update
        self.user_data = user_data
        self.bot_constants = BotConstants()
        self.bot_variables = BotVariables()
        self.query = self.update.callback_query
        self.chosen_option = self.query.data
        self.chat_id = self.query.message.chat_id
        self.message_id = self.query.message.message_id
        self.telegram_username = self.query.message.chat.username
        self.strava_telegram_webhooks_resource = StravaTelegramWebhooksResource()
        self.approve_payment_config = {
            "bot": {

            },
            "challenges": {
                "cadence90": {
                    "odd": {
                        "column_name": "odd_challenges"
                    }
                }
            }
        }

    def process(self):
        approved_payment_details = (self.chosen_option.split("payment_approved_", 1)[1]).split("_")
        category = approved_payment_details[0]
        company = approved_payment_details[1]
        month = approved_payment_details[2]
        name = approved_payment_details[3]
        athlete_id = approved_payment_details[4]
        if self.strava_telegram_webhooks_resource.approve_payment_for_challenge(
                self.approve_payment_config[category][company][month]['column_name'], athlete_id):
            message = "Approved payment for {name} ({athlete_id}).".format(name=name, athlete_id=athlete_id)
            self.strava_telegram_webhooks_resource.update_challenges_stats(athlete_id)
        else:
            message = "Failed to approve payment for {name} ({athlete_id}).".format(name=name, athlete_id=athlete_id)
        logging.info(message)
        self.bot.edit_message_text(text=message, chat_id=self.chat_id, message_id=self.message_id)
