#  -*- encoding: utf-8 -*-

from os import sys, path

from stravalib import unithelper

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.operations import Operations


class RideMiscStats(object):
    def __init__(self):
        self.operations = Operations()

    @staticmethod
    def input():
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

    @staticmethod
    def output():
        return "*Strava:*\n\n" \
               "- _Using Since_: {using_since}\n" \
               "- _Following Count_: {following_count}\n" \
               "- _Followers Count_: {followers_count}\n" \
               "- _Kudos Received_: {kudos_count}\n" \
               "- _Total Achievements_: {total_achievements}\n" \
               "- _Private Rides_: {private_rides}\n" \
               "- _Flagged Rides_: {flagged_rides}\n" \
               "\n*Rides:*\n\n" \
               "- _Biggest Ride_: {biggest_ride}\n" \
               "- _Max Elevation Gain_: {max_elevation_gain}\n" \
               "- _Non-Stop Rides_: {non_stop_rides}\n" \
               "- _Calories Burnt_: {calories_burnt}\n" \
               "\n*Speed:*\n\n" \
               "- _Max Speed_: {max_speed}\n" \
               "- _Best Avg Speed_: {best_avg_speed}\n"

    @staticmethod
    def output_bikes(output_ride_misc_stats, bikes):
        output_ride_misc_stats += "*\n\nBike(s):*\n\n{bikes}\n".format(bikes=bikes)
        return output_ride_misc_stats

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
            pass

        return message

    def calculate_athlete_info(self, input_ride_misc_stats, athlete_info):
        input_ride_misc_stats['following'] = athlete_info.friend_count
        input_ride_misc_stats['followers'] = athlete_info.follower_count
        input_ride_misc_stats['strava_created'] = athlete_info.created_at.date()
        input_ride_misc_stats['bikes'] = self.get_bikes_info(athlete_info)
        return input_ride_misc_stats

    def calculate(self, input_ride_misc_stats, activity):
        if not self.operations.is_flagged_or_private(activity):
            input_ride_misc_stats['kudos'] += activity.kudos_count
            input_ride_misc_stats['achievement_count'] += activity.achievement_count
            if (int(activity.distance) >= 50000.0) and ((unithelper.timedelta_to_seconds(
                    activity.elapsed_time) - unithelper.timedelta_to_seconds(activity.moving_time)) <= 900):
                input_ride_misc_stats['non_stop'] += 1

            if float(unithelper.kilometers_per_hour(activity.max_speed)) > input_ride_misc_stats['max_speed']:
                input_ride_misc_stats['max_speed'] = float(unithelper.kilometers_per_hour(activity.max_speed))
                input_ride_misc_stats['max_speed_activity'] = activity.id

            if float(unithelper.kilometers_per_hour(activity.average_speed)) > input_ride_misc_stats['max_avg_speed']:
                input_ride_misc_stats['max_avg_speed'] = float(unithelper.kilometers_per_hour(activity.average_speed))
                input_ride_misc_stats['max_avg_speed_activity'] = activity.id

            if activity.device_watts and activity.average_watts:
                if activity.average_watts > input_ride_misc_stats['average_watts']:
                    input_ride_misc_stats['average_watts'] = activity.average_watts
                    input_ride_misc_stats['average_watts_activity'] = activity.id
                if activity.max_watts > input_ride_misc_stats['max_watts']:
                    input_ride_misc_stats['max_watts'] = activity.max_watts
                    input_ride_misc_stats['max_watts_activity'] = activity.id

            if activity.has_heartrate and (activity.max_heartrate > input_ride_misc_stats['max_heart_rate']):
                input_ride_misc_stats['max_heart_rate'] = activity.max_heartrate
                input_ride_misc_stats['max_heart_rate_activity'] = activity.id

            if activity.average_cadence and (activity.average_cadence > input_ride_misc_stats['average_cadence']):
                input_ride_misc_stats['average_cadence'] = activity.average_cadence
                input_ride_misc_stats['average_cadence_activity'] = activity.id

            if float(activity.distance) > input_ride_misc_stats['biggest_ride']:
                input_ride_misc_stats['biggest_ride'] = float(activity.distance)
                input_ride_misc_stats['biggest_ride_activity'] = activity.id

            if int(activity.total_elevation_gain) > input_ride_misc_stats['max_elevation_gain']:
                input_ride_misc_stats['max_elevation_gain'] = int(activity.total_elevation_gain)
                input_ride_misc_stats['max_elevation_gain_activity'] = activity.id

            if activity.kilojoules:
                input_ride_misc_stats['kilojoules'] += activity.kilojoules
        else:
            if activity.flagged:
                input_ride_misc_stats['flagged'] += 1

            if activity.private:
                input_ride_misc_stats['private'] += 1

        return input_ride_misc_stats

    def format(self, input_ride_misc_stats):
        output_ride_misc_stats = self.output()
        output_ride_misc_stats = output_ride_misc_stats.format(
            using_since=input_ride_misc_stats['strava_created'],
            following_count=input_ride_misc_stats['following'],
            followers_count=input_ride_misc_stats['followers'],
            kudos_count=input_ride_misc_stats['kudos'],
            total_achievements=input_ride_misc_stats['achievement_count'],
            private_rides=input_ride_misc_stats['private'],
            flagged_rides=input_ride_misc_stats['flagged'],
            biggest_ride=self.operations.strava_activity_hyperlink().format(
                text="{value} km".format(
                    value=self.operations.meters_to_kilometers(input_ride_misc_stats['biggest_ride'])),
                activity_id=input_ride_misc_stats['biggest_ride_activity']),
            max_elevation_gain=self.operations.strava_activity_hyperlink().format(
                text="{value} meters".format(
                    value=self.operations.remove_decimal_point(input_ride_misc_stats['max_elevation_gain'])),
                activity_id=input_ride_misc_stats['max_elevation_gain_activity']),
            non_stop_rides=input_ride_misc_stats['non_stop'],
            calories_burnt=self.operations.remove_decimal_point(input_ride_misc_stats['kilojoules']),
            max_speed=self.operations.strava_activity_hyperlink().format(
                text="{value} km/h".format(
                    value=input_ride_misc_stats['max_speed']),
                activity_id=input_ride_misc_stats['max_speed_activity']),
            best_avg_speed=self.operations.strava_activity_hyperlink().format(
                text="{value} km/h".format(
                    value=self.operations.round_off_two_decimal_places(input_ride_misc_stats['max_avg_speed'])),
                activity_id=input_ride_misc_stats['max_avg_speed_activity']))

        if input_ride_misc_stats['bikes'] != "":
            output_ride_misc_stats = self.output_bikes(output_ride_misc_stats, input_ride_misc_stats['bikes'])

        return output_ride_misc_stats
