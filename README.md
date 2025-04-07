# Ultrasound Image Processor

This application processes ultrasound images to make the baby appear dark against a bright background, which can be useful for creating tactile representations or improving visibility.

## Features

- Upload ultrasound images (JPEG or PNG)
- Process images to enhance contrast and make the baby more visible
- View original and processed images side by side
- Download processed images

## Processing Steps

The application performs the following steps on each image:

1. **Color Inversion**: Makes the baby appear dark and the surrounding fluid bright
2. **Contrast Enhancement**: Uses CLAHE (Contrast Limited Adaptive Histogram Equalization) to improve contrast
3. **Edge Preservation**: Applies a bilateral filter to reduce noise while preserving edges
4. **Adaptive Thresholding**: Separates dark and light areas using local thresholding
5. **Morphological Operations**: Enhances dark areas through dilation and erosion
6. **Final Thresholding**: Ensures dark areas are solid black

## Installation

1. Make sure you have Python 3.8 or later installed on your system.

2. Clone this repository:
```bash
git clone <repository-url>
cd ultrasound-a11y
```

3. Create a virtual environment (recommended):
```bash
python -m venv venv
```

4. Activate the virtual environment:
- On Windows:
```bash
.\venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

5. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure your virtual environment is activated (if you're using one)

2. Run the application:
```bash
shiny run app.py
```

3. Open your web browser and go to:
```
http://127.0.0.1:8000
```

## Usage

1. Click the "Upload Ultrasound Image" button to select an image file
2. The original and processed images will appear side by side
3. To download the processed image, click the "Download Processed Image" button
4. The processed image will be saved with "processed_" prefix

## Technical Details

The application uses:
- Shiny for Python for the web interface
- OpenCV for image processing
- NumPy for numerical operations

## Troubleshooting

If you encounter any issues:

1. Make sure all required packages are installed:
```bash
pip install -r requirements.txt
```

2. If you get a Python version error, try using Python 3.8 or 3.9

3. If the application doesn't start, try running with a different port:
```bash
shiny run app.py --port 8080
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
