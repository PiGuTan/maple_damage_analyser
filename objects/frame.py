from .cropped_frame import CroppedFrame
from .mask import Mask
from util import save_to_file
from pathlib import Path
import argparse
import csv

masks:list[Mask] = []

frame_parser = argparse.ArgumentParser(add_help=False)
frame_parser.add_argument('--mask_dir', type=str, default="masks", help="directory to masks")
frame_parser.add_argument("--debug_full", action="store_true", help="saves full extracted frame in --debug_dir")
frame_parser.add_argument('--debug_dir', default=None, help="if set saves ocr input to directory")
frame_parser.add_argument('--output', default="result.csv", help="sets output file")
args, _ = frame_parser.parse_known_args()

result_header = ["timestamp"]

class Frame:
    def __init__(self, frame, frame_time):
        self.frame = frame
        self.frame_time = frame_time
        self.cropped_frames: list[CroppedFrame] = []

    def crop_frame(self):
        if args.debug_full and args.debug_dir:
            save_to_file(f"{args.debug_dir}/{self.frame_time:.2f}_full.png", self.frame)
        for mask in masks:
            x_start = mask.x
            y_start = mask.y
            x_end = x_start + mask.w
            y_end = mask.y + mask.h
            cropped_frame = self.frame[y_start:y_end, x_start:x_end]
            self.cropped_frames.append(CroppedFrame(cropped_frame, mask.method, mask.header_name))
            if args.debug_dir:
                save_to_file(f"{args.debug_dir}/{self.frame_time:.2f}_{mask.header_name}.png",cropped_frame)

    def read_frame(self):
        result_row = [f"{self.frame_time:.2f}"]
        for frame in self.cropped_frames:
            result_row.extend(frame.read_frame())
        with open(args.output, "a", newline="", encoding="utf-8") as f:
            row_writer = csv.writer(f)
            row_writer.writerows([result_row])

directory_path = Path(args.mask_dir)
for file_path in directory_path.iterdir():
    if file_path.is_file():
        new_mask = Mask(file_path)
        masks.append(new_mask)
        result_header.extend((new_mask.header_name,f"{new_mask.header_name}_prob"))
with open(args.output, "w", newline="", encoding="utf-8") as f:
    header_writer = csv.writer(f)
    header_writer.writerows([result_header])