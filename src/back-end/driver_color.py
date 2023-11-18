import concurrent.futures
import cProfile
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

    @lru_cache(maxsize=None)
    def calculate_histograms(self, image_path, resize=True, target_size=(64, 64)):
        if image_path in self.histogram_cache:
            return self.histogram_cache[image_path]

        image = cv2.imread(image_path)

        if resize:
            image = cv2.resize(image, target_size)

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv_image], [0, 1, 2], None, [8, 12, 3], [0, 180, 0, 256, 0, 256])
        self.histogram_cache[image_path] = hist
        return hist

    def calculate_cosine_similarity(self, hist1, hist2):
        hist1 = hist1.flatten()
        hist2 = hist2.flatten()
        dot_product = np.dot(hist1, hist2)
        magnitude1 = np.linalg.norm(hist1)
        magnitude2 = np.linalg.norm(hist2)
        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity

    def process_image(self, image2_path):
        hist2 = self.calculate_histograms(image2_path)
        similarity = self.calculate_cosine_similarity(hist1, hist2)
        return image2_path, similarity
    

    def compare_images_in_folder(self, folder_path):
        global hist1
        hist1 = self.calculate_histograms(self.image1_path)

        similar_images = []  # Memindahkan similar_images ke sini untuk menyimpan semua gambar
        highest_similarity = -1

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_image, os.path.join(folder_path, filename))
                       for filename in os.listdir(folder_path)
                       if filename.endswith(('.jpg', '.jpeg', '.png'))]

            for future in concurrent.futures.as_completed(futures):
                image2_path, similarity = future.result()

                if similarity > 0.6:
                    similar_images.append((image2_path, similarity))  # Menambahkan semua gambar dengan similarity > 0.6

                if similarity > highest_similarity:
                    highest_similarity = similarity

        similar_images.sort(key=lambda x: x[1], reverse=True)

        # if save_path and similar_images:
        #     with open(save_path, 'w') as file:
        #         for path, sim in similar_images:
        #             file.write(path + '\n' + "cosine similarity: " + str(round(sim * 100, 2)) + '%' + '\n')

        return similar_images, highest_similarity

def get_similar_images():
    current_directory = os.getcwd()

    # Mengganti path dengan path relatif terhadap direktori saat ini
    image1_path = os.path.join('database/image', 'image.jpg')
    image_folder = os.path.join('database/dataset')
    

    comparator = ImageComparator(image1_path)
    similar_images, highest_similarity = comparator.compare_images_in_folder(image_folder)

    similar_images_data = []

    if similar_images:
        for path, sim in similar_images:
            if sim > 0.6:
                path.replace
                similar_images_data.append({"image_url": path, "similarity": sim * 100})

    if similar_images_data:
        return similar_images_data
    else:
        return {"message": "No similar images found with similarity above 0.6."}