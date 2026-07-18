import easyocr
import objects.custom_exceptions

reader = easyocr.Reader(['en'])

class CroppedFrame:
    def method_mapping(self,method_name):
        method_mapping = {
            "pct": self.read_frame_pct,
        }
        if method_name not in method_mapping:
            raise objects.custom_exceptions.UnknownMethod(method_name)
        return method_mapping[method_name]

    def __init__(self,frame,method_name, header_name):
        self.frame = frame
        self.method = self.method_mapping(method_name)
        self.header_name = header_name

    def read_frame(self) -> (str,float):
        """
        generic method to read frame
        :return: string and confidence read from easyocr
        """
        return self.method()

    def read_frame_pct(self)-> (str,float):
        result = reader.readtext(self.frame,
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
        #for (bbox, text, prob) in result:
            #return text, prob
        if not result or len(result) == 0:
            return "", 1
        highest = max(result, key=lambda x: x[2])
        return highest[1], highest[2]