#  -*- encoding: utf-8 -*-

from datetime import date
from os import sys, path

from stravalib.client import Client

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from stravalib import unithelper

from scripts.common.common import Common


class RideStats(object):

    @staticmethod
    def calculate_ride_stats(current_year, activity, all_time_ride_stats, ytd_ride_stats):

        activity_year = activity.start_date_local.year

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

        return all_time_ride_stats, ytd_ride_stats


class StatsFormat(object):

    def __init__(self):
        self.common = Common()

    def all_time_ride_stats(self):
        return {
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

    def ytd_ride_stats(self):
        return {
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

    def populate_ride_stats(self, all_time_ride_stats, ytd_ride_stats):
        return "*All Time Stats:*\n\n" \
               "- _Rides_: {rides} (Includes {indoor_rides} Indoors)\n" \
               "- _Distance_: {distance} km (Includes {indoor_distance} km of Indoors)\n" \
               "- _Moving Time_: {moving_time} hours (Includes {indoor_time} hours of Indoors)\n" \
               "- _Elevation Gain_: {elevation_gain} km\n" \
               "- _50's_: {fifties}\n" \
               "- _100's_: {hundreds} (Includes {one_hundred_fifties} _150's_ & {two_hundreds} _200's_)\n\n" \
               "*Year to Date Stats:*\n\n" \
               "- _Rides_: {ytd_rides} (Includes {ytd_indoor_rides} Indoors)\n" \
               "- _Distance_: {ytd_distance} km (Includes {ytd_indoor_distance} km of Indoors)\n" \
               "- _Moving Time_: {ytd_moving_time} hours (Includes {ytd_indoor_time} hours of Indoors)\n" \
               "- _Elevation Gain_: {ytd_elevation_gain} km\n" \
               "- _50's_: {ytd_fifties}\n" \
               "- _100's_: {ytd_hundreds} (Includes {ytd_one_hundred_fifties} _150's_ & {ytd_two_hundreds} _200's_)".format(
            rides=all_time_ride_stats['rides'],
            indoor_rides=all_time_ride_stats['indoor_rides'],
            distance=self.common.meters_to_kilometers(
                                                                             all_time_ride_stats['distance']),
            indoor_distance=self.common.meters_to_kilometers(
                                                                             all_time_ride_stats['indoor_distance']),
            moving_time=self.common.seconds_to_human_readable(
                                                                             all_time_ride_stats['moving_time']),
            indoor_time=self.common.seconds_to_human_readable(
                                                                             all_time_ride_stats['indoor_time']),
            elevation_gain=self.common.meters_to_kilometers(
                                                                             all_time_ride_stats['elevation_gain']),
            fifties=all_time_ride_stats['fifties'],
            hundreds=all_time_ride_stats['hundreds'],
            one_hundred_fifties=all_time_ride_stats['one_hundred_fifties'],
            two_hundreds=all_time_ride_stats['two_hundreds'],
            ytd_rides=ytd_ride_stats['rides'],
            ytd_indoor_rides=ytd_ride_stats['indoor_rides'],
            ytd_distance=self.common.meters_to_kilometers(
                                                                             ytd_ride_stats['distance']),
            ytd_indoor_distance=self.common.meters_to_kilometers(
                                                                             ytd_ride_stats['indoor_distance']),
            ytd_moving_time=self.common.seconds_to_human_readable(
                                                                             ytd_ride_stats['moving_time']),
            ytd_indoor_time=self.common.seconds_to_human_readable(
                                                                             ytd_ride_stats['indoor_time']),
            ytd_elevation_gain=self.common.meters_to_kilometers(
                                                                             ytd_ride_stats['elevation_gain']),
            ytd_fifties=ytd_ride_stats['fifties'],
            ytd_hundreds=ytd_ride_stats['hundreds'],
            ytd_one_hundred_fifties=ytd_ride_stats['one_hundred_fifties'],
            ytd_two_hundreds=ytd_ride_stats['two_hundreds'])


class Stats(object):

    def __init__(self, athlete_token):
        self.common = Common()
        self.strava_client = Client()
        self.strava_client.access_token = athlete_token

    def main(self):
        current_year = date.today().year
        activities = self.strava_client.get_activities()

        all_stats = []
        stats_format = StatsFormat()
        all_time_ride_stats = stats_format.all_time_ride_stats()
        ytd_ride_stats = stats_format.ytd_ride_stats()

        ride_stats_class = RideStats()

        for activity in activities:
            if not self.common.is_flagged_or_private(activity):
                if self.common.is_activity_a_ride(activity):
                    all_time_ride_stats, ytd_ride_stats = ride_stats_class.calculate_ride_stats(current_year, activity,
                                                                                                all_time_ride_stats,
                                                                                                ytd_ride_stats)

        if all_time_ride_stats['rides'] > 0:
            ride_stats = stats_format.populate_ride_stats(all_time_ride_stats, ytd_ride_stats)
            all_stats.append(ride_stats)

        return all_stats
