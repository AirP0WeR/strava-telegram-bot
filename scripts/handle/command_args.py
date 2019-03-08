#  -*- encoding: utf-8 -*-

import logging
import traceback
from collections import defaultdict

import requests

from clients.database import DatabaseClient
from common.constants_and_variables import BotConstants, BotVariables
from resources.strava_telegram_webhooks import StravaTelegramWebhooksResource


class HandleCommandArgs(object):

    def __init__(self, bot, update, args):
        self.bot = bot
        self.update = update
        self.args = args
        self.bot_constants = BotConstants()
        self.bot_variables = BotVariables()
        self.strava_telegram_webhooks_resource = StravaTelegramWebhooksResource()
        self.database_client = DatabaseClient()

    def default(self):
        pass

    def token_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            athlete_token = self.strava_telegram_webhooks_resource.get_token(athlete_id)
            if athlete_token:
                message = "Token for {athlete_id}: `{athlete_token}`".format(athlete_id=athlete_id,
                                                                             athlete_token=athlete_token)
            else:
                message = "Athlete ID {athlete_id} not found.".format(athlete_id=athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.shadow_message(message)
        else:
            logging.warning("More than 1 arguments passed for /token. Args {}".format(self.args))

    def activate_athlete_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            try:
                self.database_client.write_operation(
                    self.bot_constants.QUERY_ACTIVATE_ATHLETE.format(athlete_id=athlete_id))
            except Exception:
                message = "Failed to activate {athlete_id}. Exception: {exception}".format(athlete_id=athlete_id,
                                                                                           exception=traceback.format_exc())
            else:
                message = "Successfully activated {athlete_id}".format(athlete_id=athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.shadow_message(message)
        else:
            logging.warning("More than 1 arguments passed for /activate. Args {}".format(self.args))

    def deactivate_athlete_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            try:
                self.database_client.write_operation(
                    self.bot_constants.QUERY_DEACTIVATE_ATHLETE.format(athlete_id=athlete_id))
            except Exception:
                message = "Failed to deactivate {athlete_id}. Exception: {exception}".format(athlete_id=athlete_id,
                                                                                             exception=traceback.format_exc())
            else:
                message = "Successfully deactivated {athlete_id}".format(athlete_id=athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.shadow_message(message)
        else:
            logging.warning("More than 1 arguments passed for /deactivate. Args {}".format(self.args))

    def update_stats_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            response = requests.post(self.bot_variables.api_update_stats_webhook.format(athlete_id=athlete_id))
            if response.status_code == 200:
                message = "Updating stats for {}..".format(athlete_id)
            else:
                message = "Failed to trigger update stats for {}".format(athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.shadow_message(message)
        else:
            logging.warning("More than 1 arguments passed for /deactivate. Args {}".format(self.args))

    def process(self):
        command = self.update.message.text.split(' ', 1)[0]

        options = defaultdict(lambda: self.default, {
            '/token': self.token_command,
            '/activate': self.activate_athlete_command,
            '/deactivate': self.deactivate_athlete_command,
            '/update': self.update_stats_command
        })

        options[command]()
