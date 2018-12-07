#  -*- encoding: utf-8 -*-

from os import sys, path

from stravalib import unithelper

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.operations import Operations


class RunYtdStats(object):
    def __init__(self):
        self.operations = Operations()

    @staticmethod
    def input():
        return {
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

    @staticmethod
    def output():
        return "*Run - Year to Date Stats:*\n\n" \
               "- _Runs_: {ytd_time_runs}\n" \
               "- _Distance_: {ytd_time_distance} km\n" \
               "- _Moving Time_: {ytd_time_moving_time} hours\n" \
               "- _Elevation Gain_: {ytd_time_elevation_gain} km\n" \
               "- _5's_: {ytd_time_five}\n" \
               "- _10's_: {ytd_time_ten}\n" \
               "- _HM's_: {ytd_time_hm}\n" \
               "- _FM's_: {ytd_time_fm}\n" \
               "- _Ultra's_: {ytd_time_ultra}\n\n"

    def calculate(self, input_run_ytd_stats, activity, current_year):
        if not self.operations.is_flagged_or_private(activity):
            activity_year = activity.start_date_local.year
            if activity_year == current_year:
                input_run_ytd_stats['runs'] += 1
                input_run_ytd_stats['moving_time'] += unithelper.timedelta_to_seconds(activity.moving_time)
                input_run_ytd_stats['elevation_gain'] += int(activity.total_elevation_gain)
                input_run_ytd_stats['distance'] += float(activity.distance)
                if 5000.0 <= float(activity.distance) < 10000.0:
                    input_run_ytd_stats['five'] += 1
                elif 10000.0 <= float(activity.distance) < 21000.0:
                    input_run_ytd_stats['ten'] += 1
                elif 21000.0 < float(activity.distance) < 42000.0:
                    input_run_ytd_stats['hm'] += 1
                elif 42000.0 < float(activity.distance) < 44000.0:
                    input_run_ytd_stats['fm'] += 1
                elif float(activity.distance) > 44000.0:
                    input_run_ytd_stats['ultra'] += 1

        return input_run_ytd_stats

    def format(self, input_run_ytd_stats):
        output_run_ytd_stats = self.output()
        return output_run_ytd_stats.format(
            ytd_time_runs=input_run_ytd_stats['runs'],
            ytd_time_distance=self.operations.meters_to_kilometers(input_run_ytd_stats['distance']),
            ytd_time_moving_time=self.operations.seconds_to_human_readable(input_run_ytd_stats['moving_time']),
            ytd_time_elevation_gain=self.operations.meters_to_kilometers(input_run_ytd_stats['elevation_gain']),
            ytd_time_five=input_run_ytd_stats['five'],
            ytd_time_ten=input_run_ytd_stats['ten'],
            ytd_time_hm=input_run_ytd_stats['hm'],
            ytd_time_fm=input_run_ytd_stats['fm'],
            ytd_time_ultra=input_run_ytd_stats['ultra'])
