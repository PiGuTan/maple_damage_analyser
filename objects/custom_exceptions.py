class UnknownMethod(Exception):
    def __init__(self, method_name):
        super().__init__(f"Method '{method_name}' not found. add it to 'method_mapping' in 'cropped_frame.py'")

class UnknownIconType(Exception):
    def __init__(self, icon_type):
        super().__init__(f"Icon type '{icon_type}' was not defined. Recheck in 'cropped_frame.py'")