import logging

from common import Common
from strava_api import StravaApi


class Segments(StravaApi, Common):
    stats_format = "*%s. %s*\n\n*Personal Record:*\nTime: %s\nDate: %s\nTotal Attempts: %s\n\n*Segment Details:*\nDistance: %s kms\nCreated: %s\nAvg Gradient: %s percent\nMax Gradient: %s percent\nHighest Elevation: %s meters\nLowest Elevation: %s meters\nTotal Elevation Gain: %s meters\nTotal Athletes Attempted: %s\nTotal Attempts: %s\n\n*Leaderboard*:\n%s" + "\n\n"

    leaderboard_format = "%s. %s | %s | %s\n"

    def __init__(self, athlete_token):
        logging.info("Initializing %s" % self.__class__.__name__)
        StravaApi.__init__(self, athlete_token)

    def prepare_leaderboard(self, leaderboard):
        message = ""
        for leader in leaderboard['entries']:
            message += (self.leaderboard_format
                        % (leader['rank'],
                           self.seconds_to_human_readable(leader['elapsed_time']),
                           self.date_to_human_readable_with_time(leader['start_date_local']),
                           leader['athlete_name']))
        return message

    def collect_stats(self, starred_segments):
        segment_stats = ""
        segment_count = 1
        for segment in starred_segments:
            segment_details = self.get_segment_details(segment['id'])
            segment_leaderboard = self.get_segment_leaderboard(segment['id'], "1", "10")
            segment_stats += (self.stats_format %
                              (
                                  segment_count,
                                  segment['name'],
                                  self.seconds_to_human_readable(segment['athlete_pr_effort']['elapsed_time']),
                                  self.date_to_human_readable_with_time(
                                      segment['athlete_pr_effort']['start_date_local']),
                                  segment_details['athlete_segment_stats']['effort_count'],
                                  self.meters_to_kilometers(segment['distance']),
                                  self.date_to_human_readable(segment_details['created_at']),
                                  segment['average_grade'],
                                  segment['maximum_grade'],
                                  segment['elevation_high'],
                                  segment['elevation_low'],
                                  segment_details['total_elevation_gain'],
                                  segment_details['athlete_count'],
                                  segment_details['effort_count'],
                                  self.prepare_leaderboard(segment_leaderboard)
                              ))
            segment_count += 1

        return segment_stats

    def main(self):
        message = "You don't have any starred segments."
        starred_segments = self.get_starred_segments("200", "1")
        if len(starred_segments) > 1:
            message = self.collect_stats(starred_segments)

        return message
