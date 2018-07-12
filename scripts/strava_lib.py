import logging

from stravalib.client import Client


class StravaLib(object):

    def __init__(self, athlete_token):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.athlete_token = athlete_token
        self.client = Client()
        self.client.access_token = self.athlete_token

    def get_athlete(self):
        return self.client.get_athlete()

    def get_activities(self):
        return self.client.get_activities()

    def get_starred_segments(self):
        return self.client.get_starred_segment()

    def get_segment_details(self, segment_id):
        return self.client.get_segment(segment_id)

    def get_segment_leader_board(self, segment_id):
        return self.client.get_segment_leaderboard(segment_id)
