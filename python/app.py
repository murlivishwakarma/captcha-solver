from flask import Flask, request, jsonify
import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
import concurrent.futures  # Allows parallel execution
import sys
app = Flask(__name__)

# Set Tesseract Path
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


# Function to preprocess image
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# Function to solve CAPTCHA
def solve_captcha(image):
    processed_image = preprocess_image(image)
    return pytesseract.image_to_string(processed_image, config="--psm 8").strip()

# API Route for CAPTCHA solving (Multiple Requests Supported)
@app.route("/solve_captcha", methods=["POST"])
def solve_captcha_endpoint():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    image = Image.open(file.stream)
    image_np = np.array(image)

    # Process CAPTCHA in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(solve_captcha, image_np)
        captcha_text = future.result()

    return jsonify({"captcha_text": captcha_text})

if __name__ == "__main__":
      
        app.run(host="127.0.0.1", port=4000, threaded=True)  # ✅ Supports multiple requests
