import re
from pathlib import Path
import cv2

def time_to_seconds(time_str: str) -> int:
    """
    Converts a time string in format 'mm:ss' or 'xxmxxs' into total integer seconds.
    Completely ignores hours.
    """
    clean_str = time_str.strip().lower()
    if any(char in clean_str for char in ['m', 's']):
        minutes = re.search(r'(\d+)\s*m', clean_str)
        seconds = re.search(r'(\d+)\s*s', clean_str)
        total_seconds = 0
        if minutes:
            total_seconds += int(minutes.group(1)) * 60
        if seconds:
            total_seconds += int(seconds.group(1))
        return total_seconds
    if ':' in clean_str:
        parts = list(map(int, clean_str.split(':')))
        return parts[-2] * 60 + parts[-1]
    try:
        return int(clean_str)
    except ValueError:
        raise ValueError(f"Could not parse time format: '{time_str}'")

def save_to_file(path:str, img):
    full_path = Path(path)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(path, img)