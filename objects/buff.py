import cv2
from pathlib import Path

class Buff:
    def __init__(self, file_path:Path):
        self.icon = cv2.imread(file_path)
        file_name = file_path.name.split('.',maxsplit=1)[0]
        self.buff_name = file_name

buffs:list[Buff] = []
debuffs:list[Buff] = []
