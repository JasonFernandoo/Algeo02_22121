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
    
    def calculate_histograms(self, image_path, resize=True, target_size=(64, 64)):
        if image_path in self.histogram_cache:
            return self.histogram_cache[image_path]
        
        image = self.load_and_resize_image(image_path, resize, target_size)
        hsv_image = self.rgb_to_hsv(image)
        hist = self.calculate_manual_histogram(hsv_image)
        self.histogram_cache[image_path] = hist
        return hist
    
    def load_and_resize_image(self, image_path, resize, target_size):
        image = self.read_image(image_path)
        if resize:
            image = self.resize_image(image, target_size)
        return image
    
    def read_image(self, image_path):
        img = open(image_path, "rb").read()
        nparr = np.frombuffer(img, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image
    
    def resize_image(self, image, target_size):
        # Resizing image without using built-in function
        resized_image = np.zeros((target_size[0], target_size[1], 3), dtype=np.uint8)
        for i in range(target_size[0]):
            for j in range(target_size[1]):
                resized_image[i, j] = image[int(i * (len(image) / target_size[0])), int(j * (len(image[0]) / target_size[1]))]
        return resized_image
    
    def rgb_to_hsv(self, image):
        # Manual RGB to HSV conversion
        hsv_image = np.zeros_like(image, dtype=np.float32)
        for i in range(len(image)):
            for j in range(len(image[0])):
                r, g, b = image[i, j]
                r, g, b = r / 255.0, g / 255.0, b / 255.0
                
                cmax = max(r, g, b)
                cmin = min(r, g, b)
                delta = cmax - cmin
                
                if delta == 0:
                    h = 0
                elif cmax == r:
                    h = (60 * ((g - b) / delta) + 360) % 360
                elif cmax == g:
                    h = (60 * ((b - r) / delta) + 120) % 360
                else:
                    h = (60 * ((r - g) / delta) + 240) % 360
                
                if cmax == 0:
                    s = 0
                else:
                    s = (delta / cmax) * 100
                
                v = cmax * 100
                
                hsv_image[i, j] = np.array([h, s, v], dtype=np.float32)
        
        return hsv_image
    
    def calculate_manual_histogram(self, hsv_image):
        # Manual histogram calculation
        hist_bins = [8, 12, 3]
        hist = np.zeros((hist_bins[0], hist_bins[1], hist_bins[2]))

        h, w, _ = hsv_image.shape
        
        for y in range(h):
            for x in range(w):
                pixel = hsv_image[y, x]
                h_idx = int(pixel[0] / 360 * hist_bins[0])
                s_idx = int(pixel[1] / 100 * hist_bins[1])
                v_idx = int(pixel[2] / 100 * hist_bins[2])

                if h_idx == hist_bins[0]:
                    h_idx -= 1
                if s_idx == hist_bins[1]:
                    s_idx -= 1
                if v_idx == hist_bins[2]:
                    v_idx -= 1

                hist[h_idx, s_idx, v_idx] += 1
        
        return hist

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
            futures = [executor.submit(self.process_image, os.path.join(folder_path, filename))
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