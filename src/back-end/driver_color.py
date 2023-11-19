import concurrent.futures
import cv2
import numpy as np
import os
import json
import time
from functools import lru_cache
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

start_time = time.time()

class ImageComparator:
    def __init__(self, image1_path):
        self.image1_path = image1_path
        self.histogram_cache = {}

    def calculate_histograms(self, image_path, resize=True, target_size=(64, 64)):
        if image_path in self.histogram_cache:
            return self.histogram_cache[image_path]

        image = self.read_image(image_path)
        if resize:
            image = self.resize_image(image, target_size)
        hsv_image = self.rgb_to_hsv(image)
        # hist = self.calculate_manual_histogram(hsv_image)
        hist = cv2.calcHist([hsv_image], [0, 1, 2], None, [8, 12, 3], [0, 360, 0, 100, 0, 100])
        cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

        self.histogram_cache[image_path] = hist
        return hist

    @staticmethod
    def read_image(image_path):
        img = open(image_path, "rb").read()
        nparr = np.frombuffer(img, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image

    @staticmethod
    def resize_image(image, target_size):
        resized_image = cv2.resize(image, target_size)
        return resized_image
    

    # def rgb_to_hsv(self, image):
    #     r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    #     r, g, b = r / 255.0, g / 255.0, b / 255.0

    #     cmax = np.maximum(np.maximum(r, g), b)
    #     cmin = np.minimum(np.minimum(r, g), b)
    #     delta = cmax - cmin

    #     h = np.zeros_like(cmax)
        
    #     # Calculate h values avoiding zero division and adjusting conditions
    #     mask = delta != 0
    #     cond1 = cmax == r
    #     cond2 = cmax == g
        
    #     # h[mask & cond1] = (60 * ((g - b) / delta) + 360) % 360
    #     # h[mask & cond2] = (60 * ((b - r) / delta) + 120) % 360
    #     # h[mask & ~cond1 & ~cond2] = (60 * ((r - g) / delta) + 240) % 360
        
    #     h[mask & cond1] = (60 * (((g - b) / delta)[mask & cond1] % 6))
    #     h[mask & cond2] = (60 * (((b - r) / delta)[mask & cond2] + 2))
    #     h[mask & ~cond1 & ~cond2] = (60 * (((r - g) / delta)[mask & ~cond1 & ~cond2] + 4))

    #     s = np.zeros_like(cmax)
    #     s[cmax != 0] = (delta / cmax)[cmax != 0] * 100

    #     v = cmax * 100

    #     hsv_image = np.dstack((h, s, v)).astype(np.float32)
    #     return hsv_image
    def rgb_to_hsv(self, image):
        r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
        r, g, b = r / 255.0, g / 255.0, b / 255.0

        cmax = np.maximum(np.maximum(r, g), b)
        cmin = np.minimum(np.minimum(r, g), b)
        delta = cmax - cmin

        h = np.zeros_like(cmax)
        s = np.zeros_like(cmax)
        v = np.zeros_like(cmax)

        mask = delta != 0
        not_zero_delta = mask

        cond1 = cmax == r
        cond2 = cmax == g

        h[mask & cond1] = (60 * (((g - b) / delta)[mask & cond1] % 6))
        h[mask & cond2] = (60 * (((b - r) / delta)[mask & cond2] + 2))
        h[mask & ~cond1 & ~cond2] = (60 * (((r - g) / delta)[mask & ~cond1 & ~cond2] + 4))

        s[not_zero_delta] = (delta / cmax)[not_zero_delta] * 100

        v[cmax != 0] = cmax[cmax != 0] * 100

        hsv_image = np.dstack((h, s, v)).astype(np.float32)
        return hsv_image


        
    # def calculate_manual_histogram(self, hsv_image):
    #     # Optimized histogram calculation using NumPy operations
    #     hist_bins = [8, 12, 3]
    #     h, s, v = hsv_image[:, :, 0], hsv_image[:, :, 1], hsv_image[:, :, 2]

    #     h_idx = (h / 360 * hist_bins[0]).astype(np.int)
    #     s_idx = (s / 100 * hist_bins[1]).astype(np.int)
    #     v_idx = (v / 100 * hist_bins[2]).astype(np.int)

    #     h_idx = np.clip(h_idx, 0, hist_bins[0] - 1)
    #     s_idx = np.clip(s_idx, 0, hist_bins[1] - 1)
    #     v_idx = np.clip(v_idx, 0, hist_bins[2] - 1)

    #     hist = np.zeros((hist_bins[0], hist_bins[1], hist_bins[2]))

    #     for i in range(hsv_image.shape[0]):
    #         for j in range(hsv_image.shape[1]):
    #             hist[h_idx[i, j], s_idx[i, j], v_idx[i, j]] += 1
        
    #     return hist

    def calculate_cosine_similarity(self, hist1, hist2):
        # Calculating cosine similarity manually
        hist1 = hist1.flatten()
        hist2 = hist2.flatten()
        dot_product = np.dot(hist1, hist2)
        magnitude1 = np.linalg.norm(hist1)
        magnitude2 = np.linalg.norm(hist2)
        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity
    
    def process_image(self, image2_path):
        hist1 = self.calculate_histograms(self.image1_path)
        hist2 = self.calculate_histograms(image2_path)
        similarity = self.calculate_cosine_similarity(hist1, hist2)
        return image2_path, similarity

    def compare_images_in_folder(self, folder_path):
        similar_images = []
        highest_similarity = -1

        hist1 = self.calculate_histograms(self.image1_path)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_image, (folder_path + "/" + filename))
                       for filename in os.listdir(folder_path)
                       if filename.endswith(('.jpg', '.jpeg', '.png'))]

            for future in concurrent.futures.as_completed(futures):
                image2_path, similarity = future.result()

                if similarity > 0.6:
                    similar_images.append((image2_path, similarity))

                if similarity > highest_similarity:
                    highest_similarity = similarity

        similar_images.sort(key=lambda x: x[1], reverse=True)

        return similar_images, highest_similarity


def get_similar_color():
    current_directory = os.getcwd()

    image1_path = "static/image/image.jpg"
    image_folder = "static/dataset"

    comparator = ImageComparator(image1_path)
    similar_images, highest_similarity = comparator.compare_images_in_folder(image_folder)

    similar_images_data = []

    if similar_images:
        for path, sim in similar_images:
            if sim > 0.6:
                similar_images_data.append({"image_url": path, "similarity": sim * 100})

    if similar_images_data:
        return similar_images_data
    else:
        return {"message": "No similar images found with similarity above 0.6."}