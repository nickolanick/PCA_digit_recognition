from digit_matrix_detection.performRecognition import DigitDetection


class DetectMatrix:
    def __init__(self, detection_cls):
        self.detection_cls = detection_cls


matrix_detector = DetectMatrix(DigitDetection("digits_cls2.pkl"))
