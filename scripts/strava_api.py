import logging

import requests


class StravaApi(object):
    url_strava_api = "https://www.strava.com/api/v3"

    def __init__(self, athlete_token):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.athlete_token = athlete_token

    def get_athlete_info(self):
        response = requests.get(self.url_strava_api + "/athlete", headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()

    def get_athlete_stats(self, athlete_id):
        response = requests.get(self.url_strava_api + "/athletes/%s/stats" % athlete_id,
                                headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()

    def get_athlete_activities(self, total_activities, page):
        response = requests.get(
            self.url_strava_api + "/athlete/activities?per_page=%s&page=%s" % (total_activities, page),
            headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()

    def get_starred_segments(self, total_activities, page):
        response = requests.get(
            self.url_strava_api + "/segments/starred?page=%s&per_page=%s" % (page, total_activities),
            headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()

    def get_segment_details(self, segment_id):
        response = requests.get(self.url_strava_api + "/segments/%s" % segment_id, headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()

    def get_segment_leaderboard(self, segment_id, page, per_page):
        response = requests.get(
            self.url_strava_api + "/segments/%s/leaderboard?page=%s&per_page=%s" % (segment_id, page, per_page),
            headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()
