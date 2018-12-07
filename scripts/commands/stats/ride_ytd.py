#  -*- encoding: utf-8 -*-

from os import sys, path

from stravalib import unithelper

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.operations import Operations


class RideYtdStats(object):
    def __init__(self):
        self.operations = Operations()

    @staticmethod
    def input():
        return {
            'rides': 0,
            'indoor_rides': 0,
            'distance': 0,
            'indoor_distance': 0,
            'moving_time': 0,
            'indoor_moving_time': 0,
            'elevation_gain': 0,
            'fifties': 0,
            'hundreds': 0,
            'one_hundred_fifties': 0,
            'two_hundreds': 0
        }

    @staticmethod
    def output():
        return "*Ride - Year to Date Stats:*\n\n" \
               "- _Rides_: {ytd_rides} (Includes {ytd_indoor_rides} Indoors)\n" \
               "- _Distance_: {ytd_distance} km (Includes {ytd_indoor_distance} km of Indoors)\n" \
               "- _Moving Time_: {ytd_moving_time} hours (Includes {ytd_indoor_moving_time} hours of Indoors)\n" \
               "- _Elevation Gain_: {ytd_elevation_gain} km\n" \
               "- _50's_: {ytd_fifties}\n" \
               "- _100's_: {ytd_hundreds} (Includes {ytd_one_hundred_fifties} _150's_ & {ytd_two_hundreds} _200's_)"

    def calculate(self, input_ride_ytd_stats, activity, current_year):
        if not self.operations.is_flagged_or_private(activity):
            activity_year = activity.start_date_local.year
            if activity_year == current_year:
                input_ride_ytd_stats['rides'] += 1
                input_ride_ytd_stats['moving_time'] += unithelper.timedelta_to_seconds(activity.moving_time)
                input_ride_ytd_stats['elevation_gain'] += int(activity.total_elevation_gain)
                input_ride_ytd_stats['distance'] += float(activity.distance)
                if self.operations.is_indoor(activity):
                    input_ride_ytd_stats['indoor_distance'] += float(activity.distance)
                    input_ride_ytd_stats['indoor_moving_time'] += unithelper.timedelta_to_seconds(activity.moving_time)
                    input_ride_ytd_stats['indoor_rides'] += 1
                if 50000.0 <= float(activity.distance) < 100000.0:
                    input_ride_ytd_stats['fifties'] += 1
                elif 100000.0 <= float(activity.distance) < 150000.0:
                    input_ride_ytd_stats['hundreds'] += 1
                elif 150000.0 < float(activity.distance) < 200000.0:
                    input_ride_ytd_stats['one_hundred_fifties'] += 1
                    input_ride_ytd_stats['hundreds'] += 1
                elif float(activity.distance) > 200000.0:
                    input_ride_ytd_stats['two_hundreds'] += 1
                    input_ride_ytd_stats['hundreds'] += 1

        return input_ride_ytd_stats

    def format(self, input_ride_ytd_stats):
        output_ride_ytd_stats = self.output()
        return output_ride_ytd_stats.format(
            ytd_rides=input_ride_ytd_stats['rides'],
            ytd_indoor_rides=input_ride_ytd_stats['indoor_rides'],
            ytd_distance=self.operations.meters_to_kilometers(input_ride_ytd_stats['distance']),
            ytd_indoor_distance=self.operations.meters_to_kilometers(input_ride_ytd_stats['indoor_distance']),
            ytd_moving_time=self.operations.seconds_to_human_readable(input_ride_ytd_stats['moving_time']),
            ytd_indoor_moving_time=self.operations.seconds_to_human_readable(
                input_ride_ytd_stats['indoor_moving_time']),
            ytd_elevation_gain=self.operations.meters_to_kilometers(input_ride_ytd_stats['elevation_gain']),
            ytd_fifties=input_ride_ytd_stats['fifties'],
            ytd_hundreds=input_ride_ytd_stats['hundreds'],
            ytd_one_hundred_fifties=input_ride_ytd_stats['one_hundred_fifties'],
            ytd_two_hundreds=input_ride_ytd_stats['two_hundreds'])
