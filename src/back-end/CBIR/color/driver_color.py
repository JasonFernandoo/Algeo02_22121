import concurrent.futures
import cProfile
import cv2
import numpy as np
import os
import time
from functools import lru_cache

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

    def compare_images_in_folder(self, folder_path, save_path=None):
        global hist1
        hist1 = self.calculate_histograms(self.image1_path)

        similar_images = []
        similar_percent = []
        most_similar_images = []
        highest_similarity = -1

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_image, os.path.join(folder_path, filename))
                       for filename in os.listdir(folder_path)
                       if filename.endswith(('.jpg', '.jpeg', '.png'))]

            for future in concurrent.futures.as_completed(futures):
                image2_path, similarity = future.result()

                if similarity > 0.6:
                    similar_images.append((image2_path, similarity))
                    similar_percent.append(similarity)

                if similarity > highest_similarity:
                    highest_similarity = similarity
                    most_similar_images = [(image2_path, similarity)]
                elif similarity == highest_similarity:
                    most_similar_images.append((image2_path, similarity))

        # Sort similar images by similarity (high to low)
        similar_images.sort(key=lambda x: x[1], reverse=True)

        i = 0
        if save_path and similar_images:
            with open(save_path, 'w') as file:
                for path, sim in similar_images:
                    file.write(path + '\n' + "cosine similarity: " + str(round(sim * 100, 2)) + '%' + '\n')
                    i += 1

        return most_similar_images, highest_similarity

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    image1_path = 'C:/Users/jonat/Documents/Koding Santuy/Algeoasik/Algeo02_22121/src/back-end/image/search/105.jpg'
    image_folder = 'C:/Users/jonat/Documents/Koding Santuy/Algeoasik/Algeo02_22121/src/back-end/image/dataset'
    save_path = 'C:/Users/jonat/Documents/Koding Santuy/Algeoasik/Algeo02_22121/src/back-end/CBIR/color/similar_color.txt' 

    comparator = ImageComparator(image1_path)
    similar_images, highest_similarity = comparator.compare_images_in_folder(image_folder, save_path)

    if similar_images:
        print("Most similar images:")
        for path, sim in similar_images:
            print(path, "Cosine Similarity:", sim * 100, "%")
    else:
        print("No similar images found with similarity above 0.6.")

    # Stop profiling and print the results
    profiler.disable()
    profiler.print_stats(sort='cumulative')

    end_time = time.time()
    execution_time = end_time - start_time
    print("Waktu eksekusi:", execution_time, "detik")