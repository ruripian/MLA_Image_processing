import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

def extract_pattern_grid(image_path, min_size, padding_x, padding_y):
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = [cv2.boundingRect(contour) for contour in contours]

    max_size = 100 
    filtered_boxes = [
        box for box in bounding_boxes if min_size < box[2] < max_size and min_size < box[3] < max_size
    ]

    filtered_boxes = sorted(filtered_boxes, key=lambda b: (b[1], b[0]))

    if filtered_boxes:
        center_x, center_y = gray.shape[1] // 2, gray.shape[0] // 2

        distances = [
            ((box[0] + box[2] // 2 - center_x) ** 2 + (box[1] + box[3] // 2 - center_y) ** 2, box)
            for box in filtered_boxes
        ]
        distances.sort()
        central_box = distances[0][1]

        box_width, box_height = central_box[2], central_box[3]

        start_x = central_box[0] - (box_width + padding_x)
        start_y = central_box[1] - (box_height + padding_y)
        pattern_grid = []

        for row in range(3):
            for col in range(3):
                x = start_x + col * (box_width + padding_x)
                y = start_y + row * (box_height + padding_y)
                pattern_grid.append((x, y, box_width, box_height))

        output_folder = "pattern_out"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        cropped_images = []
        for i, (x, y, w, h) in enumerate(pattern_grid):
            crop = image[y : y + h, x : x + w]
            cropped_images.append(crop)
            cv2.imwrite(f"{output_folder}/pattern_{i+1}.png", crop)

        for i, crop in enumerate(cropped_images):
            plt.subplot(3, 3, i + 1)
            plt.imshow(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
            plt.axis("off")
        plt.show()
    else:
        print("No suitable patterns detected.")

image_path = "cropped_image.png"  # Replace with your image path
min_size = int(input("Enter the minimum pattern size (e.g., 20): "))
padding_x = int(input("Enter the horizontal padding between patterns: "))
padding_y = int(input("Enter the vertical padding between patterns: "))
extract_pattern_grid(image_path, min_size, padding_x, padding_y)
