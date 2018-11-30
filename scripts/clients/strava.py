#  -*- encoding: utf-8 -*-

from stravalib.client import Client


class StravaClient(object):

    def __init__(self, athlete_token):
        self.athlete_token = athlete_token

    def get_strava_client(self):
        strava_client = Client()
        strava_client.access_token = self.athlete_token
        return strava_client
