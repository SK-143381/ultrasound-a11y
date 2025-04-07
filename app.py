from shiny import App, render, ui, reactive
import cv2
import numpy as np
import os
import tempfile
from pathlib import Path
import shutil

def process_ultrasound_image(image_path):
    # Load the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Step 1: Invert the image (make baby dark, fluid bright)
    inverted = cv2.bitwise_not(image)

    # Step 2: Apply CLAHE with higher clip limit for more contrast
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(inverted)

    # Step 3: Apply bilateral filter to preserve edges while reducing noise
    bilateral = cv2.bilateralFilter(contrast_enhanced, 9, 75, 75)

    # Step 4: Apply adaptive thresholding with larger block size
    thresh = cv2.adaptiveThreshold(
        bilateral, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        21,  # Increased block size
        5    # Increased constant
    )

    # Step 5: Apply morphological operations to enhance dark areas
    kernel = np.ones((5,5), np.uint8)
    # First dilate to make dark areas larger
    dilated = cv2.dilate(thresh, kernel, iterations=2)
    # Then erode to smooth the edges
    eroded = cv2.erode(dilated, kernel, iterations=1)
    # Finally close to fill small holes
    closed = cv2.morphologyEx(eroded, cv2.MORPH_CLOSE, kernel)

    # Step 6: Apply another threshold to ensure dark areas are solid
    _, final = cv2.threshold(closed, 127, 255, cv2.THRESH_BINARY)

    # Save to a temporary file
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "processed_image.png")
    cv2.imwrite(output_path, final)
    return output_path

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_file("image", "Upload Ultrasound Image",
                     accept=[".jpg", ".jpeg", ".png"],
                     multiple=False),
        ui.hr(),
        ui.h4("Processing Steps:"),
        ui.tags.ul(
            ui.tags.li("Invert colors (make baby dark, fluid bright)"),
            ui.tags.li("Enhance contrast using CLAHE"),
            ui.tags.li("Apply bilateral filter to preserve edges"),
            ui.tags.li("Adaptive thresholding to separate dark/light areas"),
            ui.tags.li("Morphological operations to enhance dark areas"),
            ui.tags.li("Final thresholding for solid black areas")
        ),
        ui.hr(),
        ui.download_button("download", "Download Processed Image")
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Original Image"),
            ui.output_image("original")
        ),
        ui.card(
            ui.card_header("Processed Image"),
            ui.output_image("processed")
        )
    )
)

def server(input, output, session):
    @output
    @render.image
    def original():
        if input.image() is None:
            return None
        return {"src": input.image()[0]["datapath"], "width": "100%"}

    @reactive.Calc
    def processed_image():
        if input.image() is None:
            return None
        return process_ultrasound_image(input.image()[0]["datapath"])

    @output
    @render.image
    def processed():
        if processed_image() is None:
            return None
        return {"src": processed_image(), "width": "100%"}

    @session.download
    def download():
        if processed_image() is None:
            return None
        return Path(processed_image())

app = App(app_ui, server) 