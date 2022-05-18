import cv2
import cvlib as cv

def model(input_path):
    image = cv2.imread(input_path)
    box, label, count = cv.detect_common_objects(image)
    return label.count('car')
