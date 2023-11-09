from PIL import Image
import numpy as np
import cv2 as cv2
import math as math

class Search:
    
    def __init__(self, image, name):
        self.image = image

    def query_search(self):
        # Read image
        query = cv2.imdecode(np.fromstring(self.image, np.uint8), cv2.IMREAD_UNCHANGED)
        print(query)

        # Initialize ColorDescriptor and bins
        descriptor = ColorDescriptor((8, 12, 3))

        # Describe feature of query image
        feature = descriptor.describe(query)

        #print(feature)
        print(feature)

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

V = Image.open(r'src\back-end\image\search\105.jpg')
# W = Image.open(r'src\back-end\image\dataset\104.jpg')
# X = Image.open(r'src\back-end\image\dataset\105.jpg')
# Y = Image.open(r'src\back-end\image\dataset\106.jpg')

if V.mode != "RGB":
    V = V.convert("RGB") 

width, height = V.size
matrix = [[0 for x in range(width)] for y in range(height)]

V = list(V.getdata())
V = np.array(V)


for i in range(width):
    for j in range(height):
        matrix[i][j] = V[(width*(i))+j]

