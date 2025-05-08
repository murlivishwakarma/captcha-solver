from flask import Flask, request, jsonify
import os
import cv2
import numpy as np
import pytesseract
from PIL import Image
import concurrent.futures  # Allows parallel execution

app = Flask(__name__)

# Set Tesseract Path (Make sure this path is correct for your environment)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Correct path for Azure Linux environment

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

# Make sure the app listens on the correct port for Azure (use dynamic PORT variable)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set by Azure
    app.run(host="0.0.0.0", port=port, threaded=True)  # ✅ Supports multiple requests
