import logging

from scripts.client.strava_api import StravaApi


class UpdateActivity(StravaApi):

    def __init__(self, bot, update, activity_type, athlete_token):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.bot = bot
        self.update = update
        self.activity_type = activity_type
        StravaApi.__init__(self, athlete_token)

    def main(self):
        latest_activity = self.get_latest_activity()
        if self.update_activity_type(latest_activity['id'], self.activity_type):
            return "Successfully updated your latest activity to Walk."
        else:
            return "Failed to update your latest activity to Walk."
