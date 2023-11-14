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

    def compare_images_in_folder(self, folder_path, save_path):
        image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(('.jpg', '.jpeg', '.png'))]

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(self.compare_images, image_paths))

        similar_images = [(path, sim) for path, sim in zip(image_paths, results) if sim > 0.6]

        if save_path and similar_images:
            with open(save_path, 'w') as file:
                for path, sim in similar_images:
                    file.write(f"{path}\nCosine Similarity: {round(sim * 100, 2)}%\n")

        return similar_images

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    image1_path = 'C:/Users/jonat/Documents/Koding Santuy/Algeoasik/Algeo02_22121/src/back-end/image/search/105.jpg'
    image_folder = 'C:/Users/jonat/Documents/Koding Santuy/Algeoasik/Algeo02_22121/src/back-end/image/dataset'
    save_path = 'C:/Users/jonat/Documents/Koding Santuy/Algeoasik/Algeo02_22121/src/back-end/CBIR/texture/similar_texture.txt' 

    cbir = TextureCBIR(image1_path)
    similar_images = cbir.compare_images_in_folder(image_folder, save_path)
    
    if similar_images:
        print("Similar images found. Check the output file for details.")
    else:
        print("No similar images found.")

    profiler.disable()
    profiler.print_stats()

    end_time = time.time()
    print("Execution Time:", end_time - start_time, "seconds")
