#  -*- encoding: utf-8 -*-

import logging
from collections import defaultdict

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

    def default(self):
        pass

    def token_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            athlete_details = self.strava_telegram_webhooks_resource.get_athlete(athlete_id)
            if athlete_details:
                athlete_token = athlete_details['athlete_token']
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
            if self.strava_telegram_webhooks_resource.activate_flag_athlete(athlete_id=athlete_id):
                message = "Successfully activated {athlete_id}.".format(athlete_id=athlete_id)
            else:
                message = "Failed to activate {athlete_id}.".format(athlete_id=athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.shadow_message(message)
        else:
            logging.warning("More than 1 arguments passed for /activate. Args {}".format(self.args))

    def deactivate_athlete_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            if self.strava_telegram_webhooks_resource.deactivate_flag_athlete(athlete_id=athlete_id):
                message = "Successfully deactivated {athlete_id}.".format(athlete_id=athlete_id)
            else:
                message = "Failed to deactivate {athlete_id}.".format(athlete_id=athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.shadow_message(message)
        else:
            logging.warning("More than 1 arguments passed for /deactivate. Args {}".format(self.args))

    def update_stats_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            if self.strava_telegram_webhooks_resource.update_stats(athlete_id):
                message = "Updating stats for {}..".format(athlete_id)
            else:
                message = "Failed to trigger update stats for {}".format(athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.shadow_message(message)
        else:
            logging.warning("More than 1 arguments passed for /deactivate. Args {}".format(self.args))

    def challenges_refresh_stats_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            message = self.bot_constants.MESSAGE_UPDATE_STATS_CHALLENGES_FAILED
            if self.strava_telegram_webhooks_resource.update_challenges_stats(athlete_id):
                message = self.bot_constants.MESSAGE_UPDATE_STATS_CHALLENGES_SUCCESS
            self.update.message.reply_text(message, parse_mode="Markdown",
                                           disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.shadow_message(message)
        else:
            logging.warning("More than 1 arguments passed for /deactivate. Args {}".format(self.args))

    def challenges_delete_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            if self.strava_telegram_webhooks_resource.challenges_delete_athlete(athlete_id):
                message = "Successfully deauthorised and deleted {athlete_id} from challenges".format(
                    athlete_id=athlete_id)
            else:
                message = "Failed to deauthorise and delete {athlete_id} from challenges".format(athlete_id=athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown",
                                           disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.shadow_message(message)
        else:
            logging.warning("More than 1 arguments passed for /deactivate. Args {}".format(self.args))

    def process(self):
        command = self.update.message.text.split(' ', 1)[0]

        options = defaultdict(lambda: self.default, {
            '/token': self.token_command,
            '/activate': self.activate_athlete_command,
            '/deactivate': self.deactivate_athlete_command,
            '/update': self.update_stats_command,
            '/challenges_refresh_stats': self.challenges_refresh_stats_command,
            '/challenges_delete': self.challenges_delete_command
        })

        options[command]()
