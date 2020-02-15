#  -*- encoding: utf-8 -*-

import logging
from collections import defaultdict

import facebook

from common.constants_and_variables import BotConstants, BotVariables
from resources.strava_telegram_webhooks import StravaTelegramWebhooksResource


class HandleCommandArgs:
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
            self.strava_telegram_webhooks_resource.send_message(message)
        else:
            logging.warning("More than 1 arguments passed for /token. Args %s", self.args)

    def activate_athlete_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            if self.strava_telegram_webhooks_resource.activate_flag_athlete(athlete_id=athlete_id):
                message = "Successfully activated {athlete_id}.".format(athlete_id=athlete_id)
            else:
                message = "Failed to activate {athlete_id}.".format(athlete_id=athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.send_message(message)
        else:
            logging.warning("More than 1 arguments passed for /activate. Args %s", self.args)

    def deactivate_athlete_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            if self.strava_telegram_webhooks_resource.deactivate_flag_athlete(athlete_id=athlete_id):
                message = "Successfully deactivated {athlete_id}.".format(athlete_id=athlete_id)
            else:
                message = "Failed to deactivate {athlete_id}.".format(athlete_id=athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.send_message(message)
        else:
            logging.warning("More than 1 arguments passed for /deactivate. Args %s", self.args)

    def update_stats_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            if self.strava_telegram_webhooks_resource.update_stats(athlete_id):
                message = "Updating stats for {}..".format(athlete_id)
            else:
                message = "Failed to trigger update stats for {}".format(athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.send_message(message)
        else:
            logging.warning("More than 1 arguments passed for /deactivate. Args %s", self.args)

    def challenges_refresh_stats_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            message = self.bot_constants.MESSAGE_UPDATE_STATS_CHALLENGES_FAILED
            if self.strava_telegram_webhooks_resource.update_challenges_stats(athlete_id):
                message = self.bot_constants.MESSAGE_UPDATE_STATS_CHALLENGES_SUCCESS
            self.update.message.reply_text(message, parse_mode="Markdown",
                                           disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.send_message(message)
        else:
            logging.warning("More than 1 arguments passed for /deactivate. Args %s", self.args)

    def challenges_deauth_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            if self.strava_telegram_webhooks_resource.challenges_deauth_athlete(athlete_id):
                message = "Successfully deauthorised {athlete_id} from challenges".format(
                    athlete_id=athlete_id)
            else:
                message = "Failed to deauthorise {athlete_id} from challenges".format(athlete_id=athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown",
                                           disable_web_page_preview=True)
            self.strava_telegram_webhooks_resource.send_message(message)
        else:
            logging.warning("More than 1 arguments passed for /deactivate. Args %s", self.args)

    def finish_photo(self):
        logging.info("Received post finish post on Facebook: {}".format(self.args))
        logging.info("Update message: {}", self.update.message)
        if len(self.args) == 2:
            rider_no = self.args[0].strip()
            finish_time = self.args[1].strip()
            rider_name = self.RIDERS[rider_no]
            caption = "{rider_name} finished at {finish_time}\n\n.\n.\n#AudaxMysuru #AudaxIndia #Cycling #Brevet #Randonneuring #HighwayExpress300".format(
                rider_name=rider_name, finish_time=finish_time)
            rider_photo = self.bot.get_file(self.update.message.photo[-1])
            rider_photo.download("/tmp/rider_photo.jpg")
            graph = facebook.GraphAPI(access_token=self.bot_variables.facebook_token)
            graph.put_photo(image=open('/tmp/rider_photo.jpg', 'rb'), album_path='110287720378697/photos',
                            caption=caption)
            message = "Uploaded finish post for {}: {}".format(rider_no, rider_name)
            logging.info(message)
            self.strava_telegram_webhooks_resource.send_message(message)
        else:
            logging.warning("More than 2 arguments passed for /finish. Args %s", self.args)

    def process(self):
        command = self.update.message.text.split(' ', 1)[0]

        options = defaultdict(lambda: self.default, {
            '/token': self.token_command,
            '/activate': self.activate_athlete_command,
            '/deactivate': self.deactivate_athlete_command,
            '/update': self.update_stats_command,
            '/challenges_refresh_stats': self.challenges_refresh_stats_command,
            '/challenges_deauth': self.challenges_deauth_command,
            '/finish': self.finish_photo
        })

        options[command]()
