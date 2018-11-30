#  -*- encoding: utf-8 -*-

from datetime import date
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from stravalib import unithelper

from scripts.common.common import Common


class CalculateStats(object):

    def __init__(self, activities):
        self.common = Common()
        self.activities = activities

    def calculate(self, activities, all_time_ride_stats, ytd_ride_stats, all_time_run_stats, ytd_run_stats):
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

        return all_time_ride_stats, ytd_ride_stats, all_time_run_stats, ytd_run_stats

    def main(self):
        activities = self.activities

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

        all_time_ride_stats, ytd_ride_stats, all_time_run_stats, ytd_run_stats = self.calculate(activities,
                                                                                                all_time_ride_stats,
                                                                                                ytd_ride_stats,
                                                                                                all_time_run_stats,
                                                                                                ytd_run_stats)

        stats = dict()
        stats['all_time_ride_stats'] = all_time_ride_stats
        stats['ytd_ride_stats'] = ytd_ride_stats
        stats['all_time_run_stats'] = all_time_run_stats
        stats['ytd_run_stats'] = ytd_run_stats

        return stats
