from .cropped_frame import CroppedFrame
from .mask import Mask,masks
from .buff import Buff,buffs
from util import save_to_file
from pathlib import Path
import argparse
import csv


frame_parser = argparse.ArgumentParser(add_help=False)
frame_parser.add_argument('--mask_dir', type=str, default="masks", help="directory to masks")
frame_parser.add_argument("--debug_full", action="store_true", help="saves full extracted frame in --debug_dir")
frame_parser.add_argument('--debug_dir', default=None, help="if set saves ocr input to directory")
frame_parser.add_argument('--buff_dir', default="buff_icons", help="buff icon directory storing the details on buffs")
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
buff_path = Path(args.buff_dir)
for file_path in directory_path.iterdir():
    if file_path.is_file():
        try:
            new_mask = Mask(file_path)
            masks.append(new_mask)
        except Exception as e:
            print(f"unable to create mask from {file_path} error: {e}")
            continue
        if new_mask.method in ["pct" , "ba"]:
            result_header.extend((new_mask.header_name,f"{new_mask.header_name}_prob"))
            continue
        if new_mask.header_name == "buff_icon":
            for buff_path in buff_path.iterdir():
                if buff_path.is_file():
                    new_buff = Buff(buff_path)
                    buffs.append(new_buff)
                    result_header.extend([f"{new_buff.buff_name}_buff",f"{new_buff.buff_name}_prob"])
            continue
        print(f"unknown file handling method: {new_mask.method} header_name: {new_mask.header_name} for {file_path}")



with open(args.output, "w", newline="", encoding="utf-8") as f:
    header_writer = csv.writer(f)
    header_writer.writerows([result_header])