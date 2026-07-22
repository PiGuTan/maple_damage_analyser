import easyocr
import objects.custom_exceptions
import cv2
import numpy as np
from util import find_similarity_in_big_image
from .buff import Buff,buffs,debuffs


reader = easyocr.Reader(['en'], gpu=True)

class CroppedFrame:
    def method_mapping(self,method_name):
        method_mapping = {
            "pct": self.read_frame_pct,
            "ba": self.read_frame_ba,
            "icon": self.detect_icon,
        }
        if method_name not in method_mapping:
            raise objects.custom_exceptions.UnknownMethod(method_name)
        return method_mapping[method_name]

    def __init__(self,frame,method_name, header_name):
        self.frame = frame
        self.method = self.method_mapping(method_name)
        self.header_name = header_name

    def read_frame(self):
        """
        generic method to read frame or detect icon(s) in frame
        :return: string and confidence read from easyocr
        :return: tuple of bools with their associated confidence
        """
        return self.method()

    def read_frame_pct(self)-> (str,str):
        results = reader.readtext(self.frame, #TODO: move values to config
                                 allowlist="0123456789.",
                                 mag_ratio=1.5,  # Keeps image enlarged to separate close pixel groups
                                 contrast_ths=1,
                                 text_threshold=0.2,  # Lowered to help pick up the faint, blurry '1'
                                 low_text=0.2,  # Allows low-confidence pixel clumps to register as text
                                 link_threshold=0.2,
                                 # Lower link threshold prevents characters from bleeding into each other
                                 width_ths=0.2,  # Forces strict horizontal separation so '1' doesn't merge into '0'
                                 adjust_contrast=1,  # Boosts contrast to separate white text from the orange gradient
                                 filter_ths = 0.001,
                                 )
        if not results or len(results) == 0:
            return "", 1
        highest = max(results, key=lambda x: x[2])
        return highest[1], f"{highest[2]:.3f}"
    def read_frame_ba(self)-> (str,str):
        allowlists = {
            "ctime_ba":"0123456789:",
            "dmg_ba":"0123456789,k", # to implement mbtq
        }
        allowlist = allowlists.get(self.header_name,"0123456789")
        hsv_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        # TODO: move values to config
        lower_yellow = np.array([30, 100, 100])
        upper_yellow = np.array([70, 255, 255])
        mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        isolated_color_image = cv2.bitwise_and(self.frame, self.frame, mask=mask)
        results = reader.readtext(isolated_color_image,allowlist=allowlist)

        if not results or len(results) == 0:
            return "", 1
        highest = max(results, key=lambda x: x[2])
        return highest[1], f"{highest[2]:.3f}"
    def detect_icon(self)-> list:
        csv_sub_writer = []
        match self.header_name.split("_",maxsplit=1)[0]: # in case someone want to change the word icon
            case "buff":
                active_effects = buffs
            case "debuff":
                active_effects = debuffs
            case _:
                raise objects.custom_exceptions.UnknownIconType(self.header_name)
        for buff in active_effects:
            index, prob = find_similarity_in_big_image(buff.icon,self.frame, confidence= 0.4)
            csv_sub_writer.extend((index, prob))
        return csv_sub_writer


