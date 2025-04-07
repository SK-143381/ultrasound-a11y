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

    # Step 2: Apply CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(inverted)

    # Step 3: Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(contrast_enhanced, (3, 3), 0)

    # Step 4: Sharpen the image to bring out edges
    kernel = np.array([[0, -1, 0],
                       [-1, 5,-1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(blurred, -1, kernel)

    # Save to a temporary file
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "processed_image.png")
    cv2.imwrite(output_path, sharpened)
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
            ui.tags.li("Reduce noise with Gaussian blur"),
            ui.tags.li("Sharpen edges")
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