class UnknownMethod(Exception):
    def __init__(self, method_name):
        super().__init__("Method '{}' not found. add it to 'method_mapping' in 'cropped_frame.py'".format(method_name))