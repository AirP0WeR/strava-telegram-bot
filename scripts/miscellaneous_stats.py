import logging

from stravalib import unithelper

from common import Common
from strava_lib import StravaLib


class MiscellaneousStats(StravaLib, Common):

    def __init__(self, athlete_token):
        logging.info("Initializing %s" % self.__class__.__name__)
        StravaLib.__init__(self, athlete_token)

    @staticmethod
    def get_bikes_info(athlete_info):
        bikes = athlete_info.bikes
        message = ""
        try:
            for bike in bikes:
                if message == "":
                    message += "- _%s_: %s" % (bike.name, unithelper.kilometers(bike.distance))
                else:
                    message += "\n- _%s_: %s" % (bike.name, unithelper.kilometers(bike.distance))
        except KeyError, e:
            logging.info("Key error: %s" % e)
        return message

    def calculate_stats(self, activities, stats):
        for activity in activities:
            if not self.is_flagged_or_private(activity):
                if activity.type == 'Ride' or activity.type == 'VirtualRide':

                    stats['kudos'] += activity.kudos_count
                    stats['achievement_count'] += activity.achievement_count
                    stats['break_time'] += unithelper.timedelta_to_seconds(
                        activity.elapsed_time) - unithelper.timedelta_to_seconds(activity.moving_time)

                    if (int(activity.distance) >= 50000.0) and (
                            (unithelper.timedelta_to_seconds(activity.elapsed_time) - unithelper.timedelta_to_seconds(
                                activity.moving_time)) <= 900):
                        stats['non_stop'] += 1

                    if float(unithelper.kilometers_per_hour(activity.max_speed)) > stats['max_speed']:
                        stats['max_speed'] = float(unithelper.kilometers_per_hour(activity.max_speed))
                        stats['max_speed_activity'] = activity.id

                    if float(unithelper.kilometers_per_hour(activity.average_speed)) > stats['max_avg_speed']:
                        stats['max_avg_speed'] = float(unithelper.kilometers_per_hour(activity.average_speed))
                        stats['max_avg_speed_activity'] = activity.id

                    if activity.device_watts and activity.average_watts:
                        if activity.average_watts > stats['average_watts']:
                            stats['average_watts'] = activity.average_watts
                            stats['average_watts_activity'] = activity.id
                        if activity.max_watts > stats['max_watts']:
                            stats['max_watts'] = activity.max_watts
                            stats['max_watts_activity'] = activity.id

                    if activity.has_heartrate and (activity.max_heartrate > stats['max_heart_rate']):
                        stats['max_heart_rate'] = activity.max_heartrate
                        stats['max_heart_rate_activity'] = activity.id

                    if activity.average_cadence and (activity.average_cadence > stats['average_cadence']):
                        stats['average_cadence'] = activity.average_cadence
                        stats['average_cadence_activity'] = activity.id

                    if float(activity.distance) > stats['biggest_ride']:
                        stats['biggest_ride'] = float(activity.distance)
                        stats['biggest_ride_activity'] = activity.id

                    if int(activity.total_elevation_gain) > stats['max_elevation_gain']:
                        stats['max_elevation_gain'] = int(activity.total_elevation_gain)
                        stats['max_elevation_gain_activity'] = activity.id

                    if activity.kilojoules:
                        stats['kilojoules'] += activity.kilojoules

            elif activity.type == 'Ride' or activity.type == 'VirtualRide':

                if activity.flagged:
                    stats['flagged'] += 1

                if activity.private:
                    stats['private'] += 1

        return stats

    def get_stats(self):
        stats = {
            'biggest_ride': 0,
            'biggest_ride_activity': '',
            'max_elevation_gain': 0,
            'max_elevation_gain_activity': '',
            'non_stop': 0,
            'max_avg_speed': 0.0,
            'max_avg_speed_activity': '',
            'max_speed': 0.0,
            'max_speed_activity': '',
            'average_watts': 0.0,
            'average_watts_activity': '',
            'max_watts': 0,
            'max_watts_activity': '',
            'max_heart_rate': 0,
            'max_heart_rate_activity': '',
            'average_cadence': 0.0,
            'average_cadence_activity': '',
            'achievement_count': 0,
            'following': 0,
            'followers': 0,
            'strava_created': '',
            'private': 0,
            'flagged': 0,
            'break_time': 0,
            'kudos': 0,
            'bikes': '',
            'kilojoules': 0.0
        }

        athlete_info = self.fetch_athlete()

        stats['following'] = athlete_info.friend_count
        stats['followers'] = athlete_info.follower_count
        stats['strava_created'] = athlete_info.created_at.date()
        stats['bikes'] = self.get_bikes_info(athlete_info)

        activities = self.fetch_activities()

        stats = self.calculate_stats(activities, stats)

        return stats

    def main(self):
        stats = self.get_stats()
        message = "*Strava:*\n\n" \
                  "- _Using Since_: %s\n" \
                  "- _Following Count_: %s\n" \
                  "- _Followers Count_: %s\n" \
                  "- _Kudos Received_: %s\n" \
                  "- _Total Achievements_: %s\n" \
                  "- _Private Rides_: %s\n" \
                  "- _Flagged Rides_: %s\n" \
                  "\n*Rides:*\n\n" \
                  "- _Biggest Ride_: %s\n" \
                  "- _Max Elevation Gain_: %s\n" \
                  "- _Non-Stop Rides_: %s\n" \
                  "- _Break Time During Rides_: %s\n" \
                  "- _Calories Burnt_: %s\n" \
                  "\n*Speed:*\n\n" \
                  "- _Max Speed_: %s\n" \
                  "- _Best Avg Speed_: %s\n" % \
                  (stats['strava_created'],
                   stats['following'],
                   stats['followers'],
                   stats['kudos'],
                   stats['achievement_count'],
                   stats['private'],
                   stats['flagged'],
                   self.strava_activity_hyperlink() % (
                       self.meters_to_kilometers(stats['biggest_ride']), 'kms', stats['biggest_ride_activity']),
                   self.strava_activity_hyperlink() % (self.remove_decimal_point(stats['max_elevation_gain']), 'meters',
                                                       stats['max_elevation_gain_activity']),
                   stats['non_stop'],
                   self.seconds_to_human_readable(stats['break_time']),
                   stats['kilojoules'],
                   self.strava_activity_hyperlink() % (stats['max_speed'], 'kph', stats['max_speed_activity']),
                   self.strava_activity_hyperlink() % (stats['max_avg_speed'], 'kph',
                                                       stats['max_avg_speed_activity']))

        if stats['max_watts'] != 0:
            message += "*\nPower:*\n\n"
            message += "- _Max Power_: %s\n" % (
                    self.strava_activity_hyperlink() % (stats['max_watts'], 'watts', stats['max_watts_activity']))
            message += "- _Best Avg Power_: %s\n" % (self.strava_activity_hyperlink() % (
                stats['average_watts'], 'watts', stats['average_watts_activity']))

        if stats['max_heart_rate'] != 0:
            message += "*\nHeart Rate:*\n\n"
            message += "- _Max Heart Rate_: %s\n" % (self.strava_activity_hyperlink() % (
                self.remove_decimal_point(stats['max_heart_rate']), 'bpm', stats['max_heart_rate_activity']))

        if stats['average_cadence'] != 0.0:
            message += "*\nCadence:*\n\n"
            message += "- _Best Avg Cadence_: %s" % (self.strava_activity_hyperlink() % (
                self.remove_decimal_point(stats['average_cadence']), '', stats['average_cadence_activity']))

        if stats['bikes'] != "":
            message += "*\n\nBike(s):*\n\n"
            message += "%s\n" % stats['bikes']

        return message
