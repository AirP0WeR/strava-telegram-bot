#  -*- encoding: utf-8 -*-

from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from scripts.common.common import Common


class FormatStats(object):

    def __init__(self, stats):
        self.common = Common()
        self.stats = stats

    def format(self, stats):
        all_time_ride_stats = "*All Time Stats:*\n\n" \
                              "- _Rides_: {rides} (Includes {indoor_rides} Indoors)\n" \
                              "- _Distance_: {distance} km (Includes {indoor_distance} km of Indoors)\n" \
                              "- _Moving Time_: {moving_time} hours (Includes {indoor_time} hours of Indoors)\n" \
                              "- _Elevation Gain_: {elevation_gain} km\n" \
                              "- _50's_: {fifties}\n" \
                              "- _100's_: {hundreds} (Includes {one_hundred_fifties} _150's_ & {two_hundreds} _200's_)".format(
            rides=stats['all_time_ride_stats']['rides'],
            indoor_rides=stats['all_time_ride_stats']['indoor_rides'],
            distance=self.common.meters_to_kilometers(
                stats['all_time_ride_stats']['distance']),
            indoor_distance=self.common.meters_to_kilometers(
                stats['all_time_ride_stats']['indoor_distance']),
            moving_time=self.common.seconds_to_human_readable(
                stats['all_time_ride_stats']['moving_time']),
            indoor_time=self.common.seconds_to_human_readable(
                stats['all_time_ride_stats']['indoor_time']),
            elevation_gain=self.common.meters_to_kilometers(
                stats['all_time_ride_stats']['elevation_gain']),
            fifties=stats['all_time_ride_stats']['fifties'],
            hundreds=stats['all_time_ride_stats']['hundreds'],
            one_hundred_fifties=stats['all_time_ride_stats']['one_hundred_fifties'],
            two_hundreds=stats['all_time_ride_stats']['two_hundreds'])

        ytd_ride_stats = "*Year to Date Stats:*\n\n" \
                         "- _Rides_: {ytd_rides} (Includes {ytd_indoor_rides} Indoors)\n" \
                         "- _Distance_: {ytd_distance} km (Includes {ytd_indoor_distance} km of Indoors)\n" \
                         "- _Moving Time_: {ytd_moving_time} hours (Includes {ytd_indoor_time} hours of Indoors)\n" \
                         "- _Elevation Gain_: {ytd_elevation_gain} km\n" \
                         "- _50's_: {ytd_fifties}\n" \
                         "- _100's_: {ytd_hundreds} (Includes {ytd_one_hundred_fifties} _150's_ & {ytd_two_hundreds} _200's_)".format(

            ytd_rides=stats['ytd_ride_stats']['rides'],
            ytd_indoor_rides=stats['ytd_ride_stats']['indoor_rides'],
            ytd_distance=self.common.meters_to_kilometers(
                stats['ytd_ride_stats']['distance']),
            ytd_indoor_distance=self.common.meters_to_kilometers(
                stats['ytd_ride_stats']['indoor_distance']),
            ytd_moving_time=self.common.seconds_to_human_readable(
                stats['ytd_ride_stats']['moving_time']),
            ytd_indoor_time=self.common.seconds_to_human_readable(
                stats['ytd_ride_stats']['indoor_time']),
            ytd_elevation_gain=self.common.meters_to_kilometers(
                stats['ytd_ride_stats']['elevation_gain']),
            ytd_fifties=stats['ytd_ride_stats']['fifties'],
            ytd_hundreds=stats['ytd_ride_stats']['hundreds'],
            ytd_one_hundred_fifties=stats['ytd_ride_stats']['one_hundred_fifties'],
            ytd_two_hundreds=stats['ytd_ride_stats']['two_hundreds'])

        all_time_run_stats = "*All Time Stats:*\n\n" \
                             "- _Runs_: {all_time_runs}\n" \
                             "- _Distance_: {all_time_distance} km\n" \
                             "- _Moving Time_: {all_time_moving_time} hours\n" \
                             "- _Elevation Gain_: {all_time_elevation_gain} km\n" \
                             "- _5's_: {all_time_five}\n" \
                             "- _10's_: {all_time_ten}\n" \
                             "- _HM's_: {all_time_hm}\n" \
                             "- _FM's_: {all_time_fm}\n" \
                             "- _Ultra's_: {all_time_ultra}".format(all_time_runs=stats['all_time_run_stats']['runs'],
                                                                    all_time_distance=self.common.meters_to_kilometers(
                                                                        stats['all_time_run_stats']['distance']),
                                                                    all_time_moving_time=self.common.seconds_to_human_readable(
                                                                        stats['all_time_run_stats']['moving_time']),
                                                                    all_time_elevation_gain=self.common.meters_to_kilometers(
                                                                        stats['all_time_run_stats']['elevation_gain']),
                                                                    all_time_five=stats['all_time_run_stats']['five'],
                                                                    all_time_ten=stats['all_time_run_stats']['ten'],
                                                                    all_time_hm=stats['all_time_run_stats']['hm'],
                                                                    all_time_fm=stats['all_time_run_stats']['fm'],
                                                                    all_time_ultra=stats['all_time_run_stats']['ultra'])

        ytd_run_stats = "*Year to Date Stats:*\n\n" \
                        "- _Runs_: {ytd_time_runs}\n" \
                        "- _Distance_: {ytd_time_distance} km\n" \
                        "- _Moving Time_: {ytd_time_moving_time} hours\n" \
                        "- _Elevation Gain_: {ytd_time_elevation_gain} km\n" \
                        "- _5's_: {ytd_time_five}\n" \
                        "- _10's_: {ytd_time_ten}\n" \
                        "- _HM's_: {ytd_time_hm}\n" \
                        "- _FM's_: {ytd_time_fm}\n" \
                        "- _Ultra's_: {ytd_time_ultra}\n\n".format(ytd_time_runs=stats['ytd_run_stats']['runs'],
                                                                   ytd_time_distance=self.common.meters_to_kilometers(
                                                                       stats['ytd_run_stats']['distance']),
                                                                   ytd_time_moving_time=self.common.seconds_to_human_readable(
                                                                       stats['ytd_run_stats']['moving_time']),
                                                                   ytd_time_elevation_gain=self.common.meters_to_kilometers(
                                                                       stats['ytd_run_stats']['elevation_gain']),
                                                                   ytd_time_five=stats['ytd_run_stats']['five'],
                                                                   ytd_time_ten=stats['ytd_run_stats']['ten'],
                                                                   ytd_time_hm=stats['ytd_run_stats']['hm'],
                                                                   ytd_time_fm=stats['ytd_run_stats']['fm'],
                                                                   ytd_time_ultra=stats['ytd_run_stats']['ultra'])

        stats['all_time_ride_stats'] = all_time_ride_stats
        stats['ytd_ride_stats'] = ytd_ride_stats
        stats['all_time_run_stats'] = all_time_run_stats
        stats['ytd_run_stats'] = ytd_run_stats

        return stats

    def main(self):
        stats = self.stats
        stats = self.format(stats)
        return stats
