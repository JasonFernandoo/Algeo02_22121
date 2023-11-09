import numpy as np
import cv2

query = cv2.imdecode(np.fromstring(self.image, np.uint8), cv2.IMREAD_UNCHANGED)

