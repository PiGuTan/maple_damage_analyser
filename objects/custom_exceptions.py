class UnknownMethod(Exception):
    def __init__(self, method_name):
        super().__init__(f"Method '{method_name}' not found. add it to 'method_mapping' in 'cropped_frame.py'")