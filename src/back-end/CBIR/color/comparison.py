from CBIR.color import ColorDescriptor
import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class Search:
    
    def __init__(self, image, name):
        self.image = image
        self.name = name

    def query_search(self):
        # Read image
        query = cv2.imdecode(np.fromstring(self.image, np.uint8), cv2.IMREAD_UNCHANGED)
        fname = self.name

        print(query)

        # Initialize ColorDescriptor and bins
        descriptor = ColorDescriptor((8, 12, 3))

        # Describe feature of query image
        feature = descriptor.describe(query)

        #print(feature)
        print(feature)