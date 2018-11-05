#  -*- encoding: utf-8 -*-

from os import sys, path

from stravalib.client import Client

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from scripts.common.common import Common


class Segments():
    stats_format = "*%s. %s*\n\n*Personal Record:*\n- _Time_: %s\n- _Date_: %s\n- _Total Attempts_: %s\n\n*Segment Details:*\n- _Distance_: %s\n- _Created_: %s\n- _Avg Gradient_: %s percent\n- _Max Gradient_: %s percent\n- _Highest Elevation_: %s\n- _Lowest Elevation_: %s\n- _Total Elevation Gain_: %s\n- _Total Athletes Attempted_: %s\n- _Total Attempts_: %s\n\n*Leader Board:*\n%s" + "\n\n"

    leader_board_format = "{rank}. {elapsed_time} | {start_date} | {athlete_name}\n"

    def __init__(self, athlete_token):
        self.common = Common()
        self.strava_client = Client()
        self.strava_client.access_token = athlete_token
        
    def prepare_leader_board(self, leader_board):
        message = ""
        for leader in leader_board.entries:
            message += (self.leader_board_format.format(rank=leader.rank,
                                                        elapsed_time=leader.elapsed_time,
                                                        start_date=leader.start_date_local.date(),
                                                        athlete_name=leader.athlete_name))
        return message

    def collect_stats(self, starred_segments):
        segment_stats = []
        segment_count = 0
        for segment in starred_segments:
            segment_count += 1
            segment_details = self.strava_client.get_segment(segment.id)
            segment_leader_board = self.strava_client.get_segment_leaderboard(segment.id)
            segment_stats.append(self.stats_format %
                                 (
                                 segment_count,
                                 segment.name,
                                 segment_details.athlete_segment_stats.pr_elapsed_time,
                                 segment_details.athlete_segment_stats.pr_date,
                                 segment_details.athlete_segment_stats.effort_count,
                                 segment.distance,
                                 segment_details.created_at.date(),
                                 segment.average_grade,
                                 segment.maximum_grade,
                                 segment.elevation_high,
                                 segment.elevation_low,
                                 segment_details.total_elevation_gain,
                                 segment_details.athlete_count,
                                 segment_details.effort_count,
                                 self.prepare_leader_board(segment_leader_board)
                             ))

        segment_stats.append(
            "Finished fetching stats for your {segment_count} starred segment(s).".format(segment_count=segment_count))
        return segment_stats

    def main(self):
        starred_segments = self.strava_client.get_starred_segments()
        segment_stats = self.collect_stats(starred_segments)
        return segment_stats
