from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import cv2
import numpy as np
import concurrent.futures  # For parallel execution

app = Flask(__name__)

# Function to preprocess the image for better OCR results
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# Function to solve the CAPTCHA using Tesseract OCR
def solve_captcha(image):
    processed_image = preprocess_image(image)
    captcha_text = pytesseract.image_to_string(processed_image, config='--psm 8').strip()
    return captcha_text

@app.route('/solve_captcha', methods=['POST'])
def solve_captcha_endpoint():
    file = request.files.get('image')  # Accept a single image per request

    if not file:
        return jsonify({"error": "No file provided"}), 400

    # Convert the uploaded file into an image
    image = Image.open(file.stream)
    image_np = np.array(image)

    # Use ThreadPoolExecutor to process the CAPTCHA asynchronously
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(solve_captcha, image_np)
        captcha_text = future.result()

    return jsonify({'captcha_text': captcha_text})

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
