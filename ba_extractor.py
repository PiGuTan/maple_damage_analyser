import objects
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(parents=[objects.video_parser, objects.frame_parser])
parser.add_argument("--file", type=str, help="path to video file")
args = parser.parse_args()

def main():
    video = objects.Video(args.file)
    for i in tqdm(video.frames):
        frame = objects.Frame(video.get_frame(i), video.get_frame_time(i))

        frame.crop_frame()
        frame.read_frame()

if __name__ == "__main__":
    main()