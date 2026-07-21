import cv2
import argparse
from util import time_to_seconds

video_parser = argparse.ArgumentParser(add_help=False)
video_parser.add_argument('--start_time', type=str, default="0", help="start time of video in seconds, mm:ss or xxmxxs")
video_parser.add_argument('--end_time', type=str, default="0", help="end time of video in seconds, mm:ss or xxmxxs")
video_parser.add_argument('--interval', type=float, default=1, help="interval between frames in seconds")
args, _ = video_parser.parse_known_args()

start_time = time_to_seconds(args.start_time)
end_time = time_to_seconds(args.end_time)

class Video:
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)

    @property
    def fps(self):
        return self.cap.get(cv2.CAP_PROP_FPS)

    @property
    def frames(self):
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = round(args.interval * self.fps)
        start_frame = round(start_time * self.fps) if start_time else 0
        end_frame = min(round((end_time + 1) * self.fps) if end_time else total_frames, total_frames)
        # +1 used in end_frame to make it inclusive of last frame
        return range(start_frame, end_frame, interval)

    def get_frame(self, frame_num:int):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = self.cap.read()
        return frame if ret else None # Returns the numpy.ndarray

    def get_frame_index_with_time_seconds(self, time_seconds:int):
        return int(time_seconds * self.fps)

    def get_frame_time(self, frame_num:int):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = self.cap.read()
        timestamp_ms = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        return timestamp_ms / 1000