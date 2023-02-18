# taking image from and using that

import cv2
import pytesseract
from flask import Flask, render_template, request, jsonify
import numpy as np
import base64


app = Flask(__name__)

# Initialize pytesseract
#pytesseract.pytesseract.tesseract_cmd = r'<path to your Tesseract executable>'

# Function to extract text from image
def extract_text(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply a threshold to the image to make the text more visible
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Apply some image processing techniques to improve the OCR accuracy
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    # Extract text using Tesseract OCR
    text = pytesseract.image_to_string(opening)
    return text

# Route to the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle image upload and text extraction
@app.route('/extract_text', methods=['POST'])
def upload_image():
    # Get the image from the POST request
    file = request.get_json()['image_data']
    #print('file', file)
    file = file.replace('data:image/png;base64,', '')
    file = base64.b64decode(file)
    #print("file to image:", file)
    # Read the image with OpenCV
    #file = cv2.imdecode
    image = cv2.imdecode(np.frombuffer(file, np.uint8), cv2.IMREAD_COLOR)
    #print("image details:", image)
    cv2.imwrite("image.jpg", image)
    image = cv2.imread("image.jpg")
    #print('image', image)
    #cv2.imshow("image",image)
    # Extract text from the image
    i = cv2.imread("im.jpg")
    text = extract_text(image)
    print("etracted text:", text)
    # Return the extracted text as JSON
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)