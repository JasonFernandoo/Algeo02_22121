import numpy as np
import cv2
import math

class ColorDescriptor:
    def __init__(self, bins):
        self.bins = bins
    
    def describe(self, image): #Mengubah image menjadi hsv
        self.image = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        features = []

        (h, w) = image.shape[:2]
        (cX, cY) = (int(w*0.5) , int(h*0.5))

        regions = [
        (0, 0, cX, cY),           # Top-left
        (cX, 0, w, cY),           # Top-center
        (w, 0, w, cY),            # Top-right
        (0, cY, cX, h),           # Middle-left
        (cX, cY, w, h),           # Middle-center
        (w, cY, w, h),            # Middle-right
        (0, h, cX, h),            # Bottom-left
        (cX, h, w, h),            # Bottom-center
        (w, h, w, h)              # Bottom-right
        ]

        for (startX, startY, endX, endY) in regions:
            maskArea = np.zeros(image.shape[:2], dtype="uint8")
            cv2.rectangle(maskArea, (startX, startY), (endX, endY), 255, -1)

            hist = self.histogram(image, maskArea)
            features.extend(hist)
        
    def histogram(self, image, mask):
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])
        dst = np.zeros(hist.shape, dtype="float")

        hist = cv2.normalize(hist, dst)
        hist = hist.flatten()

        return hist
