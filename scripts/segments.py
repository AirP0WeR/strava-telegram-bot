import logging

import telegram

from common import Common
from strava_lib import StravaLib


class Segments(StravaLib, Common):
    stats_format = "<strong>%s. %s</strong>\n\n<b>Personal Record:</b>\n- <i>Time</i>: %s\n- <i>Date</i>: %s\n- <i>Total Attempts</i>: %s\n\n<b>Segment Details:</b>\n- <i>Distance</i>: %s\n- <i>Created</i>: %s\n- <i>Avg Gradient</i>: %s percent\n- <i>Max Gradient</i>: %s percent\n- <i>Highest Elevation</i>: %s\n- <i>Lowest Elevation</i>: %s\n- <i>Total Elevation Gain</i>: %s\n- <i>Total Athletes Attempted</i>: %s\n- <i>Total Attempts</i>: %s\n\n<b>Leader Board:</b>\n%s" + "\n\n"

    leader_board_format = "%s. %s | %s | %s\n"

    def __init__(self, bot, update, athlete_token, shadow_mode, shadow_chat_id):
        logging.info("Initializing %s" % self.__class__.__name__)
        self.bot = bot
        self.update = update
        self.shadow_mode = shadow_mode
        self.shadow_chat_id = shadow_chat_id
        StravaLib.__init__(self, athlete_token)

    def send_message(self, bot, update, message):
        bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        update.message.reply_text(message, parse_mode="HTML", disable_web_page_preview=True)
        if self.shadow_mode and (
                int(self.shadow_chat_id) != int(update.message.chat_id)):
            bot.send_message(chat_id=self.shadow_chat_id, text=message,
                             parse_mode="HTML", disable_notification=True,
                             disable_web_page_preview=True)
        else:
            logging.info("Chat ID & Shadow Chat ID are the same")

    def prepare_leader_board(self, leader_board):
        message = ""
        for leader in leader_board.entries:
            message += (self.leader_board_format
                        % (leader.rank,
                           leader.elapsed_time,
                           leader.start_date_local.date(),
                           leader.athlete_name))
        return message

    def collect_stats(self, starred_segments):
        segment_count = 1
        for segment in starred_segments:
            segment_details = self.fetch_segment_details(segment.id)
            segment_leader_board = self.fetch_segment_leader_board(segment.id)
            segment_stats = (self.stats_format %
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
            segment_count += 1
            self.send_message(self.bot, self.update, segment_stats)

    def main(self):
        starred_segments = self.fetch_starred_segments()
        self.collect_stats(starred_segments)
        return "Finished fetching stats for your starred segment(s)."
