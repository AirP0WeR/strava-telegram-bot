#  -*- encoding: utf-8 -*-

import logging
from os import sys, path

from stravalib.client import Client

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from stravalib import unithelper

from scripts.common.common import Common


class CalculateMiscStats(object):

    def __init__(self):
        self.common = Common()

    @staticmethod
    def get_bikes_info(athlete_info):
        bikes = athlete_info.bikes
        message = ""
        try:
            for bike in bikes:
                if message == "":
                    message += "- _{bike_name}_: {bike_distance}".format(bike_name=bike.name,
                                                                         bike_distance=unithelper.kilometers(
                                                                             bike.distance))
                else:
                    message += "\n- _{bike_name}_: {bike_distance}".format(bike_name=bike.name,
                                                                           bike_distance=unithelper.kilometers(
                                                                               bike.distance))
        except Exception:
            logging.error("Exception!")

        return message

    def calculate_stats(self, activities, stats):
        for activity in activities:
            if not self.common.is_flagged_or_private(activity):
                if activity.type == 'Ride' or activity.type == 'VirtualRide':

                    stats['kudos'] += activity.kudos_count
                    stats['achievement_count'] += activity.achievement_count

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

    def get_athlete_info_stats(self, stats, athlete_info):
        stats['following'] = athlete_info.friend_count
        stats['followers'] = athlete_info.follower_count
        stats['strava_created'] = athlete_info.created_at.date()
        stats['bikes'] = self.get_bikes_info(athlete_info)

        return stats


class MiscStatsFormat(object):

    def __init__(self):
        self.common = Common()

    def misc_ride_stats(self):
        return {
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
            'kudos': 0,
            'bikes': '',
            'kilojoules': 0.0
        }

    def populate_misc_ride_stats(self, stats):
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
                   self.common.strava_activity_hyperlink() % (
                       self.common.meters_to_kilometers(stats['biggest_ride']), 'km', stats['biggest_ride_activity']),
                   self.common.strava_activity_hyperlink() % (
                       self.common.remove_decimal_point(stats['max_elevation_gain']), 'meters',
                       stats['max_elevation_gain_activity']),
                   stats['non_stop'],
                   stats['kilojoules'],
                   self.common.strava_activity_hyperlink() % (stats['max_speed'], 'km/h', stats['max_speed_activity']),
                   self.common.strava_activity_hyperlink() % (stats['max_avg_speed'], 'km/h',
                                                              stats['max_avg_speed_activity']))

        if stats['max_watts'] != 0:
            message += "*\nPower:*\n\n"
            message += "- _Max Power_: %s\n" % (
                    self.common.strava_activity_hyperlink() % (
                stats['max_watts'], 'watts', stats['max_watts_activity']))
            message += "- _Best Avg Power_: %s\n" % (self.common.strava_activity_hyperlink() % (
                stats['average_watts'], 'watts', stats['average_watts_activity']))

        if stats['max_heart_rate'] != 0:
            message += "*\nHeart Rate:*\n\n"
            message += "- _Max Heart Rate_: %s\n" % (self.common.strava_activity_hyperlink() % (
                self.common.remove_decimal_point(stats['max_heart_rate']), 'bpm', stats['max_heart_rate_activity']))

        if stats['average_cadence'] != 0.0:
            message += "*\nCadence:*\n\n"
            message += "- _Best Avg Cadence_: %s" % (self.common.strava_activity_hyperlink() % (
                self.common.remove_decimal_point(stats['average_cadence']), '', stats['average_cadence_activity']))

        if stats['bikes'] != "":
            message += "*\n\nBike(s):*\n\n"
            message += "{bikes}\n".format(bikes=stats['bikes'])

        return message


class MiscellaneousStats():

    def __init__(self, athlete_token):
        self.common = Common()
        self.strava_client = Client()
        self.strava_client.access_token = athlete_token

    def main(self):
        all_stats = []
        calculate_misc_stats = CalculateMiscStats()
        stats_format = MiscStatsFormat()
        stats = stats_format.misc_ride_stats()

        athlete_info = self.strava_client.get_athlete()

        stats = calculate_misc_stats.get_athlete_info_stats(stats, athlete_info)

        activities = self.strava_client.get_activities()

        stats = calculate_misc_stats.calculate_stats(activities, stats)

        all_stats.append(stats_format.populate_misc_ride_stats(stats))

        return all_stats
