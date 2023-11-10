from PIL import Image
import math as math
import cv2
import numpy as np
import os
import time
start_time = time.time()
class ImageComparator:
    def __init__(self, image1_path):
        self.image1 = cv2.imread(image1_path)

    def calculate_histograms(self, image):
        image_hist = cv2.calcHist([image], [0, 1, 2], None, [8, 12, 3], [0, 180, 0, 256, 0, 256])
        return image_hist

    def calculate_cosine_similarity(self, hist1, hist2):
        dot_product = np.dot(hist1.flatten(), hist2.flatten())
        magnitude1 = np.linalg.norm(hist1)
        magnitude2 = np.linalg.norm(hist2)
        similarity = dot_product / (magnitude1 * magnitude2)
        return similarity

    def compare_images_in_folder(self, folder_path, save_path=None):
        similar_images = []
        similar_percent = []
        most_similar_image = []
        highest_similarity = -1  # Initialize with a low value

        for filename in os.listdir(folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image2_path = os.path.join(folder_path, filename)
                image2 = cv2.imread(image2_path)
                hist1 = self.calculate_histograms(self.image1)
                hist2 = self.calculate_histograms(image2)
                similarity = self.calculate_cosine_similarity(hist1, hist2)
                print(similarity)

                i = 0
                if save_path and similar_images:
                    with open(save_path, 'w') as file:
                        for path in similar_images:
                            file.write(path + '\n' + "cosine similarity: " + str(round(similar_percent[i] * 100, 2)) + '%' + '\n')
                            i += 1

                if similarity > 0.6:
                    similar_images.append(image2_path)
                    similar_percent.append(similarity)

                if similarity > highest_similarity:
                    highest_similarity = similarity
                    most_similar_images = [image2_path]
                elif similarity == highest_similarity:
                    most_similar_images.append(image2_path)

        return most_similar_images, highest_similarity

if __name__ == "__main__":
    image1_path = 'C:/Users/attar/OneDrive/Documents/GitHub/Algeo02_22121/src/back-end/image/search/105.jpg'  # Gantilah dengan jalur lengkap menuju gambar Anda
    image_folder = 'C:/Users/attar/OneDrive/Documents/GitHub/Algeo02_22121/src/back-end/image/dataset'  # Gantilah dengan jalur lengkap ke folder yang berisi gambar-gambar
    save_path = 'C:/Users/attar/OneDrive/Documents/GitHub/Algeo02_22121/src/back-end/CBIR/color/similar_color.txt'  # Gantilah dengan jalur lengkap file penyimpanan hasil

    comparator = ImageComparator(image1_path)
    similar_images, highest_similarity = comparator.compare_images_in_folder(image_folder, save_path)

    if similar_images:
        print("Most similar images:", similar_images)
        print("Cosine Similarity:", highest_similarity * 100, "%")
    else:
        print("No similar images found with similarity above 0.6.")
end_time = time.time()
execution_time = end_time - start_time
print("Waktu eksekusi:", execution_time, "detik")
