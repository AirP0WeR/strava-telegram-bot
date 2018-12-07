#  -*- encoding: utf-8 -*-

from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class InputStats(object):
    INPUT_RIDE_ALL_TIME_STATS = {
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


class OutputStats(object):
    OUTPUT_RIDE_ALL_TIME_STATS = \
        "*All Time Stats:*\n\n" \
        "- _Rides_: {rides} (Includes {indoor_rides} Indoors)\n" \
        "- _Distance_: {distance} km (Includes {indoor_distance} km of Indoors)\n" \
        "- _Moving Time_: {moving_time} hours (Includes {indoor_moving_time} hours of Indoors)\n" \
        "- _Elevation Gain_: {elevation_gain} km\n" \
        "- _50's_: {fifties}\n" \
        "- _100's_: {hundreds} (Includes {one_hundred_fifties} _150's_ & {two_hundreds} _200's_)"
