import re
from pathlib import Path
import cv2
from skimage.metrics import structural_similarity as ssim
from colorthief import ColorThief

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


def get_similarity_score(template, screen_crop) -> float:
    # screen = cv2.resize(screen, (template.shape[1], template.shape[0]))
    score, _ = ssim(template, screen_crop, full=True)
    return score

def find_similarity_in_big_image(template,big_image, confidence = 0.4)-> (str,str):
    template_y_max = template.shape[0]
    template_x_max = template.shape[1]
    big_image_y_max = big_image.shape[0]
    big_image_x_max = big_image.shape[1]
    if big_image_y_max % template_y_max or big_image_x_max % template_x_max:
        raise ValueError(f"""
Screen crop should fit template perfectly
Screen crop dimensions (hxw):",{big_image.shape}
Template dimensions (hxw):{template.shape}
""")
    similarity_scores = []

    template_grey = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    big_image_grey = cv2.cvtColor(big_image, cv2.COLOR_BGR2GRAY)
    for y in range(0,big_image_y_max,template_y_max):
        row = int(y/template_y_max) + 1
        for x in range(0,big_image_x_max,template_x_max):
            column = int(x/template_x_max) + 1
            cropped_frame = big_image_grey[y:y+template_y_max,x:x+template_x_max]
            similarity_scores.append((f"r{row}c{column}",get_similarity_score(template_grey, cropped_frame)))
    index,max_score =  max(similarity_scores, key=lambda score: score[1])
    if max_score >= confidence:
        return index, f"{max_score:.3f}"
    return "", f"{max_score:.3f}"

def get_dominant_colour(path):
    color_thief = ColorThief(path)
    rgb_color = color_thief.get_color(quality=1)
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)
