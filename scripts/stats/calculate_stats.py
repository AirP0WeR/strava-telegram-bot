#  -*- encoding: utf-8 -*-

from datetime import date
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from stravalib import unithelper

from scripts.common.common import Common
import logging

class CalculateStats(object):

    def __init__(self, activities, athlete_info):
        self.common = Common()
        self.activities = activities
        self.athlete_info = athlete_info

    def calculate(self, activities, athlete_info, all_time_ride_stats, ytd_ride_stats, misc_ride_stats,
                  all_time_run_stats, ytd_run_stats):
        misc_ride_stats['following'] = athlete_info.friend_count
        misc_ride_stats['followers'] = athlete_info.follower_count
        misc_ride_stats['strava_created'] = athlete_info.created_at.date()
        misc_ride_stats['bikes'] = self.get_bikes_info(athlete_info)

        current_year = date.today().year

        for activity in activities:
            if not self.common.is_flagged_or_private(activity):
                activity_year = activity.start_date_local.year
                if self.common.is_activity_a_ride(activity):
                    if activity_year == current_year:
                        ytd_ride_stats['rides'] += 1
                    all_time_ride_stats['rides'] += 1

                    if activity_year == current_year:
                        ytd_ride_stats['moving_time'] += unithelper.timedelta_to_seconds(activity.moving_time)
                    all_time_ride_stats['moving_time'] += unithelper.timedelta_to_seconds(activity.moving_time)

                    if activity_year == current_year:
                        ytd_ride_stats['elevation_gain'] += int(activity.total_elevation_gain)
                    all_time_ride_stats['elevation_gain'] += int(activity.total_elevation_gain)

                    if activity_year == current_year:
                        ytd_ride_stats['distance'] += float(activity.distance)
                    all_time_ride_stats['distance'] += float(activity.distance)

                    if 50000.0 <= float(activity.distance) < 100000.0:
                        if activity_year == current_year:
                            ytd_ride_stats['fifties'] += 1
                        all_time_ride_stats['fifties'] += 1
                    elif 100000.0 <= float(activity.distance) < 150000.0:
                        if activity_year == current_year:
                            ytd_ride_stats['hundreds'] += 1
                        all_time_ride_stats['hundreds'] += 1
                    elif 150000.0 < float(activity.distance) < 200000.0:
                        if activity_year == current_year:
                            ytd_ride_stats['one_hundred_fifties'] += 1
                            ytd_ride_stats['hundreds'] += 1
                        all_time_ride_stats['one_hundred_fifties'] += 1
                        all_time_ride_stats['hundreds'] += 1
                    elif float(activity.distance) > 200000.0:
                        if activity_year == current_year:
                            ytd_ride_stats['two_hundreds'] += 1
                            ytd_ride_stats['hundreds'] += 1
                        all_time_ride_stats['two_hundreds'] += 1
                        all_time_ride_stats['hundreds'] += 1

                    if activity.trainer or activity.type == 'VirtualRide':
                        if activity_year == current_year:
                            ytd_ride_stats['indoor_distance'] += float(activity.distance)
                            ytd_ride_stats['indoor_time'] += unithelper.timedelta_to_seconds(activity.moving_time)
                            ytd_ride_stats['indoor_rides'] += 1
                        all_time_ride_stats['indoor_distance'] += float(activity.distance)
                        all_time_ride_stats['indoor_time'] += unithelper.timedelta_to_seconds(activity.moving_time)
                        all_time_ride_stats['indoor_rides'] += 1

                    misc_ride_stats['kudos'] += activity.kudos_count
                    misc_ride_stats['achievement_count'] += activity.achievement_count

                    if (int(activity.distance) >= 50000.0) and (
                            (unithelper.timedelta_to_seconds(activity.elapsed_time) - unithelper.timedelta_to_seconds(
                                activity.moving_time)) <= 900):
                        misc_ride_stats['non_stop'] += 1

                    if float(unithelper.kilometers_per_hour(activity.max_speed)) > misc_ride_stats['max_speed']:
                        misc_ride_stats['max_speed'] = float(unithelper.kilometers_per_hour(activity.max_speed))
                        misc_ride_stats['max_speed_activity'] = activity.id

                    if float(unithelper.kilometers_per_hour(activity.average_speed)) > misc_ride_stats['max_avg_speed']:
                        misc_ride_stats['max_avg_speed'] = float(unithelper.kilometers_per_hour(activity.average_speed))
                        misc_ride_stats['max_avg_speed_activity'] = activity.id

                    if activity.device_watts and activity.average_watts:
                        if activity.average_watts > misc_ride_stats['average_watts']:
                            misc_ride_stats['average_watts'] = activity.average_watts
                            misc_ride_stats['average_watts_activity'] = activity.id
                        if activity.max_watts > misc_ride_stats['max_watts']:
                            misc_ride_stats['max_watts'] = activity.max_watts
                            misc_ride_stats['max_watts_activity'] = activity.id

                    if activity.has_heartrate and (activity.max_heartrate > misc_ride_stats['max_heart_rate']):
                        misc_ride_stats['max_heart_rate'] = activity.max_heartrate
                        misc_ride_stats['max_heart_rate_activity'] = activity.id

                    if activity.average_cadence and (activity.average_cadence > misc_ride_stats['average_cadence']):
                        misc_ride_stats['average_cadence'] = activity.average_cadence
                        misc_ride_stats['average_cadence_activity'] = activity.id

                    if float(activity.distance) > misc_ride_stats['biggest_ride']:
                        misc_ride_stats['biggest_ride'] = float(activity.distance)
                        misc_ride_stats['biggest_ride_activity'] = activity.id

                    if int(activity.total_elevation_gain) > misc_ride_stats['max_elevation_gain']:
                        misc_ride_stats['max_elevation_gain'] = int(activity.total_elevation_gain)
                        misc_ride_stats['max_elevation_gain_activity'] = activity.id

                    if activity.kilojoules:
                        misc_ride_stats['kilojoules'] += activity.kilojoules

                elif self.common.is_activity_a_run(activity):
                    if activity_year == current_year:
                        ytd_run_stats['runs'] += 1
                    all_time_run_stats['runs'] += 1

                    if activity_year == current_year:
                        ytd_run_stats['moving_time'] += unithelper.timedelta_to_seconds(activity.moving_time)
                    all_time_run_stats['moving_time'] += unithelper.timedelta_to_seconds(activity.moving_time)

                    if activity_year == current_year:
                        ytd_run_stats['elevation_gain'] += int(activity.total_elevation_gain)
                    all_time_run_stats['elevation_gain'] += int(activity.total_elevation_gain)

                    if activity_year == current_year:
                        ytd_run_stats['distance'] += float(activity.distance)
                    all_time_run_stats['distance'] += float(activity.distance)

                    if 5000.0 <= float(activity.distance) < 10000.0:
                        if activity_year == current_year:
                            ytd_run_stats['five'] += 1
                        all_time_run_stats['five'] += 1
                    elif 10000.0 <= float(activity.distance) < 21000.0:
                        if activity_year == current_year:
                            ytd_run_stats['ten'] += 1
                        all_time_run_stats['ten'] += 1
                    elif 21000.0 < float(activity.distance) < 42000.0:
                        if activity_year == current_year:
                            ytd_run_stats['hm'] += 1
                        all_time_run_stats['hm'] += 1
                    elif 42000.0 < float(activity.distance) < 44000.0:
                        if activity_year == current_year:
                            ytd_run_stats['fm'] += 1
                        all_time_run_stats['fm'] += 1
                    elif float(activity.distance) > 44000.0:
                        if activity_year == current_year:
                            ytd_run_stats['ultra'] += 1
                        all_time_run_stats['ultra'] += 1

            elif self.common.is_activity_a_ride(activity):
                if activity.flagged:
                    misc_ride_stats['flagged'] += 1

                if activity.private:
                    misc_ride_stats['private'] += 1

        return all_time_ride_stats, ytd_ride_stats, misc_ride_stats, all_time_run_stats, ytd_run_stats

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

    def main(self):
        activities = self.activities
        athlete_info = self.athlete_info

        all_time_ride_stats = {
            'rides': 0,
            'indoor_rides': 0,
            'distance': 0,
            'indoor_distance': 0,
            'moving_time': 0,
            'indoor_time': 0,
            'elevation_gain': 0,
            'fifties': 0,
            'hundreds': 0,
            'one_hundred_fifties': 0,
            'two_hundreds': 0
        }

        ytd_ride_stats = {
            'rides': 0,
            'indoor_rides': 0,
            'distance': 0,
            'indoor_distance': 0,
            'moving_time': 0,
            'indoor_time': 0,
            'elevation_gain': 0,
            'fifties': 0,
            'hundreds': 0,
            'one_hundred_fifties': 0,
            'two_hundreds': 0
        }

        misc_ride_stats = {
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

        all_time_run_stats = {
            'runs': 0,
            'distance': 0.0,
            'moving_time': 0,
            'elevation_gain': 0,
            'five': 0,
            'ten': 0,
            'hm': 0,
            'fm': 0,
            'ultra': 0
        }

        ytd_run_stats = {
            'runs': 0,
            'distance': 0.0,
            'moving_time': 0,
            'elevation_gain': 0,
            'five': 0,
            'ten': 0,
            'hm': 0,
            'fm': 0,
            'ultra': 0
        }

        all_time_ride_stats, ytd_ride_stats, misc_ride_stats, all_time_run_stats, ytd_run_stats = self.calculate(
            activities, athlete_info,
            all_time_ride_stats,
            ytd_ride_stats, misc_ride_stats,
            all_time_run_stats,
            ytd_run_stats)

        stats = dict()
        stats['all_time_ride_stats'] = all_time_ride_stats
        stats['ytd_ride_stats'] = ytd_ride_stats
        stats['misc_ride_stats'] = misc_ride_stats
        stats['all_time_run_stats'] = all_time_run_stats
        stats['ytd_run_stats'] = ytd_run_stats

        return stats
