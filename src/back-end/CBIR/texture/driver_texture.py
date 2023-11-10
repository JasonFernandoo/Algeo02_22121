# import cv2
# import numpy as np
# import time
# from numba import jit
# import os

# start_time = time.time()

# @jit(nopython=True)
# def calculate_co_occurrence_matrix(image, offset, levels=16):
#     # Create a zero-initialized Co-occurrence Matrix
#     co_occurrence_matrix = np.zeros((levels, levels))

#     # Get image dimensions
#     height, width = image.shape

#     for y in range(height):
#         for x in range(width):
#             x2 = x + offset[0]
#             y2 = y + offset[1]

#             if 0 <= x2 < width and 0 <= y2 < height:
#                 i = image[y, x]
#                 j = image[y2, x2]
#                 co_occurrence_matrix[i, j] += 1

#     # Normalize the co-occurrence matrix
#     co_occurrence_matrix /= co_occurrence_matrix.sum()

#     return co_occurrence_matrix

# @jit(nopython=True)
# def calculate_contrast(co_occurrence_matrix):
#     # Calculate contrast from the co-occurrence matrix
#     levels = co_occurrence_matrix.shape[0]
#     mean = np.arange(levels).mean()
#     contrast = np.sum((np.arange(levels) - mean) ** 2 * co_occurrence_matrix)
#     return contrast

# @jit(nopython=True)
# def calculate_homogeneity(co_occurrence_matrix):
#     # Calculate homogeneity from the co-occurrence matrix
#     levels = co_occurrence_matrix.shape[0]
#     mean = np.arange(levels).mean()
#     homogeneity = np.sum(co_occurrence_matrix / (1 + np.abs(np.arange(levels) - mean)))
#     return homogeneity

# @jit(nopython=True)
# def calculate_entropy(co_occurrence_matrix):
#     # Calculate entropy from the co-occurrence matrix
#     eps = 1e-10  # Small constant to avoid log(0)
#     entropy = -np.sum(co_occurrence_matrix * np.log2(co_occurrence_matrix + eps))
#     return entropy

# class TextureCBIR:
#     def __init__(self, image1_path):
#         self.image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
#         self.image1 = self.quantize_image(self.image1)

#     def quantize_image(self, image, levels=16):
#         # Normalize the pixel values to the range [0, levels-1]
#         image = cv2.normalize(image, None, 0, levels - 1, cv2.NORM_MINMAX)
#         return image.astype(np.uint8)

#     def extract_texture_features(self, image, levels=16):
#         offsets = [(1, 0), (1, 1), (0, 1), (-1, 1)]
#         features = []

#         for offset in offsets:
#             co_occurrence_matrix = calculate_co_occurrence_matrix(image, offset, levels)
#             contrast = calculate_contrast(co_occurrence_matrix)
#             homogeneity = calculate_homogeneity(co_occurrence_matrix)
#             entropy = calculate_entropy(co_occurrence_matrix)
#             features.extend([contrast, homogeneity, entropy])

#         return features

#     def compare_images(self, image2_path):
#         image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
#         image2 = self.quantize_image(image2)

#         texture_features1 = self.extract_texture_features(self.image1)
#         texture_features2 = self.extract_texture_features(image2)

#         # Calculate Cosine Similarity between the two texture feature vectors
#         dot_product = np.dot(texture_features1, texture_features2)
#         magnitude1 = np.linalg.norm(texture_features1)
#         magnitude2 = np.linalg.norm(texture_features2)
#         similarity = dot_product / (magnitude1 * magnitude2)
#         return similarity

#     def compare_images_in_folder(self, folder_path, save_path):
#         similar_images = []

#         for filename in os.listdir(folder_path):
#             if filename.endswith(('.jpg', '.jpeg', '.png')):
#                 image2_path = os.path.join(folder_path, filename)
#                 similarity = self.compare_images(image2_path)
#                 if similarity > 0.6:  # Set similarity threshold here
#                     similar_images.append((image2_path, similarity))

#         if save_path and similar_images:
#             with open(save_path, 'w') as file:
#                 for path, sim in similar_images:
#                     file.write(f"{path}\nCosine Similarity: {round(sim * 100, 2)}%\n")

#         return similar_images

# if __name__ == "__main__":
#     image1_path = 'C:/Users/attar/OneDrive/Documents/GitHub/Algeo02_22121/src/back-end/image/search/105.jpg'  # Gantilah dengan jalur lengkap menuju gambar pertama
#     image_folder = 'C:/Users/attar/OneDrive/Documents/GitHub/Algeo02_22121/src/back-end/image/dataset'  # Gantilah dengan jalur lengkap ke folder gambar
#     save_path = 'C:/Users/attar/OneDrive/Documents/GitHub/Algeo02_22121/src/back-end/CBIR/texture/similar_texture.txt'  # Gantilah dengan jalur lengkap file penyimpanan hasil

#     cbir = TextureCBIR(image1_path)
#     similar_images = cbir.compare_images_in_folder(image_folder, save_path)

#     if similar_images:
#         print("Similar images found. Check the output file for details.")
#     else:
#         print("No similar images found.")

#     end_time = time.time()
#     print("Execution Time:", end_time - start_time, "seconds")
import cv2
import numpy as np
import time
from numba import jit
import os
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
        self.image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
        self.image1 = self.quantize_image(self.image1)
        self.histogram_cache = {}

    def quantize_image(self, image, levels=16):
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

    @lru_cache(maxsize=None)
    def calculate_histogram(self, image_path):
        if image_path in self.histogram_cache:
            return self.histogram_cache[image_path]

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = self.quantize_image(image)
        hist = self.extract_texture_features(image)
        self.histogram_cache[image_path] = hist
        return hist

    def compare_images(self, image2_path):
        image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
        image2 = self.quantize_image(image2)

        texture_features1 = self.extract_texture_features(self.image1)
        texture_features2 = self.calculate_histogram(image2_path)

        dot_product = np.dot(texture_features1, texture_features2)
        magnitude1 = np.linalg.norm(texture_features1)
        magnitude2 = np.linalg.norm(texture_features2)
        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity

    def compare_images_in_folder(self, folder_path, save_path):
        similar_images = []

        for filename in os.listdir(folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image2_path = os.path.join(folder_path, filename)
                similarity = self.compare_images(image2_path)
                if similarity > 0.6:
                    similar_images.append((image2_path, similarity))

        if save_path and similar_images:
            with open(save_path, 'w') as file:
                for path, sim in similar_images:
                    file.write(f"{path}\nCosine Similarity: {round(sim * 100, 2)}%\n")

        return similar_images

if __name__ == "__main__":
    image1_path = 'C:/Users/attar/OneDrive/Documents/GitHub/Algeo02_22121/src/back-end/image/search/105.jpg'
    image_folder = 'C:/Users/attar/OneDrive/Documents/GitHub/Algeo02_22121/src/back-end/image/dataset'
    save_path = 'C:/Users/attar/OneDrive/Documents/GitHub/Algeo02_22121/src/back-end/CBIR/texture/similar_texture.txt'

    cbir = TextureCBIR(image1_path)
    similar_images = cbir.compare_images_in_folder(image_folder, save_path)

    if similar_images:
        print("Similar images found. Check the output file for details.")
    else:
        print("No similar images found.")

    end_time = time.time()
    print("Execution Time:", end_time - start_time, "seconds")
