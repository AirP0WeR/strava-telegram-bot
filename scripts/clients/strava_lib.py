import logging

from stravalib.client import Client


class StravaLib(object):

    def __init__(self, athlete_token):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.athlete_token = athlete_token
        self.strava_client = Client()
        self.strava_client.access_token = self.athlete_token

    def fetch_athlete(self):
        return self.strava_client.get_athlete()

    def fetch_activities(self):
        return self.strava_client.get_activities()

    def fetch_starred_segments(self):
        return self.strava_client.get_starred_segments()

    def fetch_segment_details(self, segment_id):
        return self.strava_client.get_segment(segment_id)

    def fetch_segment_leader_board(self, segment_id):
        return self.strava_client.get_segment_leaderboard(segment_id)
