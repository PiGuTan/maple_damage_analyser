import cv2
import numpy as np
from pathlib import Path

upper_white = np.array([255,255,255])
lower_white = np.array([255,255,255])

class Mask:
    """
    a class used in objects only to define masked areas and method type

    method types include: (do update cropped_frame.py when adding method)
    - pct: gets single percentage from image
    not implemented
    - total-damage: gets total damage from image
    - combat-time: gets combat time from image
    - unknown name: bind icon?
    - unknown name: buff icon?
    """
    def __init__(self, file_path:Path):
        img = cv2.imread(file_path)
        white_mask = cv2.inRange(img, lower_white, upper_white)
        contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            raise Exception('no white region found')
        self.x, self.y, self.w, self.h = cv2.boundingRect(contours[0])
        file_name = file_path.name.split('.',maxsplit=1)[0]
        self.header_name = file_name
        self.method:str = file_name.split('_',maxsplit=1)[1]