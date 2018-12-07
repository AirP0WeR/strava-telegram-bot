#  -*- encoding: utf-8 -*-

from os import sys, path

from stravalib import unithelper

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from scripts.common.operations import Operations


class RunAllTimeStats(object):
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
        return "*Run - All Time Stats:*\n\n" \
               "- _Runs_: {all_time_runs}\n" \
               "- _Distance_: {all_time_distance} km\n" \
               "- _Moving Time_: {all_time_moving_time} hours\n" \
               "- _Elevation Gain_: {all_time_elevation_gain} km\n" \
               "- _5's_: {all_time_five}\n" \
               "- _10's_: {all_time_ten}\n" \
               "- _HM's_: {all_time_hm}\n" \
               "- _FM's_: {all_time_fm}\n" \
               "- _Ultra's_: {all_time_ultra}"

    def calculate(self, input_run_all_time_stats, activity):
        if not self.operations.is_flagged_or_private(activity):
            input_run_all_time_stats['runs'] += 1
            input_run_all_time_stats['moving_time'] += unithelper.timedelta_to_seconds(activity.moving_time)
            input_run_all_time_stats['elevation_gain'] += int(activity.total_elevation_gain)
            input_run_all_time_stats['distance'] += float(activity.distance)
            if 5000.0 <= float(activity.distance) < 10000.0:
                input_run_all_time_stats['five'] += 1
            elif 10000.0 <= float(activity.distance) < 21000.0:
                input_run_all_time_stats['ten'] += 1
            elif 21000.0 < float(activity.distance) < 42000.0:
                input_run_all_time_stats['hm'] += 1
            elif 42000.0 < float(activity.distance) < 44000.0:
                input_run_all_time_stats['fm'] += 1
            elif float(activity.distance) > 44000.0:
                input_run_all_time_stats['ultra'] += 1

        return input_run_all_time_stats

    def format(self, input_run_all_time_stats):
        output_run_all_time_stats = self.output()
        return output_run_all_time_stats.format(
            all_time_runs=input_run_all_time_stats['runs'],
            all_time_distance=self.operations.meters_to_kilometers(input_run_all_time_stats['distance']),
            all_time_moving_time=self.operations.seconds_to_human_readable(input_run_all_time_stats['moving_time']),
            all_time_elevation_gain=self.operations.meters_to_kilometers(input_run_all_time_stats['elevation_gain']),
            all_time_five=input_run_all_time_stats['five'],
            all_time_ten=input_run_all_time_stats['ten'],
            all_time_hm=input_run_all_time_stats['hm'],
            all_time_fm=input_run_all_time_stats['fm'],
            all_time_ultra=input_run_all_time_stats['ultra'])
