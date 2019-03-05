#  -*- encoding: utf-8 -*-

import logging
from collections import defaultdict

from common.get_athlete_token import GetAthleteToken


class HandleCommandArgs(object):

    def __init__(self, bot, update, args):
        self.bot = bot
        self.update = update
        self.args = args

    def default(self):
        pass

    def token_command(self):
        if len(self.args) == 1:
            athlete_id = self.args[0]
            get_athlete_token = GetAthleteToken()
            athlete_token = get_athlete_token.get_token(athlete_id)
            if athlete_token:
                message = "Token for {athlete_id}: {athlete_token}".format(athlete_id=athlete_id,
                                                                           athlete_token=athlete_token)
            else:
                message = "Athlete ID {athlete_id} not found.".format(athlete_id=athlete_id)
            self.update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
        else:
            logging.warning("More than 1 arguments passed for /token. Args {}".format(self.args))

    def process(self):
        command = self.update.message.text.split(' ', 1)[0]

        options = defaultdict(lambda: self.default, {
            '/token': self.token_command
        })

        options[command]()
