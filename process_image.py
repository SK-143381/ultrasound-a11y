import cv2
import numpy as np
import os
from PIL import Image
import io

def process_ultrasound_image(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Step 1: Invert the image
    inverted = cv2.bitwise_not(image)

    # Step 2: Apply CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(inverted)

    # Step 3: Apply Gaussian blur
    blurred = cv2.GaussianBlur(contrast_enhanced, (3, 3), 0)

    # Step 4: Sharpen the image
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(blurred, -1, kernel)

    # Save the processed image
    output_path = image_path.replace('.', '_processed.')
    cv2.imwrite(output_path, sharpened)
    return output_path 