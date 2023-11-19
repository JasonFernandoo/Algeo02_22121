import cv2
import numpy as np
import os
import cProfile
from numba import jit
from concurrent.futures import ThreadPoolExecutor
import time
from functools import lru_cache

start_time = time.time()
        
@jit(nopython=True)
def calculate_co_occurrence_matrix(image, offset, levels=16):
    co_occurrence_matrix = np.zeros((levels, levels))
    height, width = image.shape

    for y in range(height):
        for x in range(width):
            x2 = x + offset[0]
            y2 = y + offset[1]

            if 0 <= x2 < width and 0 <= y2 < height:
                i = image[y, x]
                j = image[y2, x2]
                co_occurrence_matrix[i, j] += 1

    co_occurrence_matrix /= co_occurrence_matrix.sum()
    return co_occurrence_matrix

@jit(nopython=True)
def calculate_contrast(co_occurrence_matrix):
    levels = co_occurrence_matrix.shape[0]
    mean = np.arange(levels).mean()
    contrast = np.sum((np.arange(levels) - mean) ** 2 * co_occurrence_matrix)
    return contrast

@jit(nopython=True)
def calculate_homogeneity(co_occurrence_matrix):
    levels = co_occurrence_matrix.shape[0]
    mean = np.arange(levels).mean()
    homogeneity = np.sum(co_occurrence_matrix / (1 + np.abs(np.arange(levels) - mean)))
    return homogeneity

@jit(nopython=True)
def calculate_entropy(co_occurrence_matrix):
    eps = 1e-10
    entropy = -np.sum(co_occurrence_matrix * np.log2(co_occurrence_matrix + eps))
    return entropy

class TextureCBIR:
    def __init__(self, image1_path):
        self.image1 = self.load_and_quantize_image(image1_path)

    def load_and_quantize_image(self, image_path, levels=16):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (64, 64))  # Resize the image to 64x64
        image = cv2.normalize(image, None, 0, levels - 1, cv2.NORM_MINMAX)
        return image.astype(np.uint8)

    def extract_texture_features(self, image, levels=16):
        offsets = [(1, 0), (1, 1), (0, 1), (-1, 1)]
        features = []

        for offset in offsets:
            co_occurrence_matrix = calculate_co_occurrence_matrix(image, offset, levels)
            contrast = calculate_contrast(co_occurrence_matrix)
            homogeneity = calculate_homogeneity(co_occurrence_matrix)
            entropy = calculate_entropy(co_occurrence_matrix)
            features.extend([contrast, homogeneity, entropy])

        return features

    @lru_cache(maxsize=128)
    def calculate_histogram(self, image_path):
        image = self.load_and_quantize_image(image_path)
        hist = self.extract_texture_features(image)
        return hist

    def compare_images(self, image2_path):
        texture_features1 = self.extract_texture_features(self.image1)
        texture_features2 = self.calculate_histogram(image2_path)

        dot_product = np.dot(texture_features1, texture_features2)
        magnitude1 = np.linalg.norm(texture_features1)
        magnitude2 = np.linalg.norm(texture_features2)
        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity

    def compare_images_in_folder(self, folder_path):
        image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(('.jpg', '.jpeg', '.png'))]

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(self.compare_images, image_paths))

        similar_images = [(path, sim) for path, sim in zip(image_paths, results) if sim > 0.6]
        similar_images.sort(key=lambda x: x[1], reverse=True)
        return similar_images

def get_similar_texture():
    current_directory = os.getcwd()

    # image1_path = os.path.join('database/image', 'image.jpg')
    # image_folder = os.path.join('database/dataset')
    # output_file_path = os.path.join(current_directory, 'driver.txt')
    image1_path = os.path.join('static/image', 'image.jpg')
    image_folder = os.path.join('static/dataset')
    output_file_path = os.path.join(current_directory, 'texture.txt')

    comparator = TextureCBIR(image1_path)
    similar_images = comparator.compare_images_in_folder(image_folder)

    similar_images_data = []

    if similar_images:
        for path, sim in similar_images:
            if sim > 0.6:
                path.replace
                similar_images_data.append({"image_url": path, "similarity": sim * 100})
                

    if similar_images_data:
        # Write results to the output file
        with open(output_file_path, 'w') as output_file:
            for data in similar_images_data:
                output_file.write(f"Image URL: {data['image_url']}, Similarity: {data['similarity']:.2f}%\n")
                
        return {"message": f"Results written to {output_file_path}"}
    else:
        return {"message": "No similar images found with similarity above 0.6."}
