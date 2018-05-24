import logging

import requests


class StravaApi(object):

    def __init__(self, athlete_token):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.athlete_token = athlete_token

    def get_athlete_info(self):
        response = requests.get("https://www.strava.com/api/v3/athlete", headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()

    def get_athlete_stats(self, athlete_id):
        response = requests.get("https://www.strava.com/api/v3/athletes/%s/stats" % athlete_id,
                                headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()

    def get_athlete_activities(self, total_activities, page):
        response = requests.get(
            "https://www.strava.com/api/v3/athlete/activities?per_page=%s&page=%s" % (total_activities, page),
            headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()

    def get_latest_activity(self):
        response = requests.get("https://www.strava.com/api/v3/athlete/activities", data=[('per_page', '1')],
                                headers=self.athlete_token)
        if response.status_code == 200:
            return response.json()[0]

    def update_activity_type(self, activity_id, activity_type):
        response = requests.put("https://www.strava.com/api/v3/activities/%s" % activity_id,
                                data=[('type', activity_type)], headers=self.athlete_token)
        if response.status_code == 200:
            return True
        else:
            return False
