import os
import io
import time

import easyocr
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import requests
import threading
import webbrowser

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Load OCR model
reader = easyocr.Reader(['en']) 

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    img = Image.open(io.BytesIO(file.read()))

    # Perform OCR
    result = reader.readtext(img, paragraph=False)

    return jsonify({"text": findCards(result)})

def findCards(bounds):
    if not bounds:
        return []
    
    name = bounds[0][1]
    conf_score = bounds[0][2]
    cards = []

    if conf_score >= 0.0:
        url = f"https://api.scryfall.com/cards/search?q=!\"{name}\""
        response = requests.get(url)

        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            for card in data.get("data", []):
                cards.append(card['name'])
    
    return cards


choices = [
    "abq",
    "ady",
    "af",
    "ang",
    "ar",
    "as",
    "ava",
    "az",
    "be",
    "bg",
    "bh",
    "bho",
    "bn",
    "bs",
    "ch_sim",
    "ch_tra",
    "che",
    "cs",
    "cy",
    "da",
    "dar",
    "de",
    "en",
    "es",
    "et",
    "fa",
    "fr",
    "ga",
    "gom",
    "hi",
    "hr",
    "hu",
    "id",
    "inh",
    "is",
    "it",
    "ja",
    "kbd",
    "kn",
    "ko",
    "ku",
    "la",
    "lbe",
    "lez",
    "lt",
    "lv",
    "mah",
    "mai",
    "mi",
    "mn",
    "mr",
    "ms",
    "mt",
    "ne",
    "new",
    "nl",
    "no",
    "oc",
    "pi",
    "pl",
    "pt",
    "ro",
    "ru",
    "rs_cyrillic",
    "rs_latin",
    "sck",
    "sk",
    "sl",
    "sq",
    "sv",
    "sw",
    "ta",
    "tab",
    "te",
    "th",
    "tjk",
    "tl",
    "tr",
    "ug",
    "uk",
    "ur",
    "uz",
    "vi"
]

def run_server():
    app.run(debug=False, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    # Start Flask in a separate thread
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    # Wait a moment to ensure the server is running
    time.sleep(1)

    # Open the local website
    dir_name = os.path.dirname(__file__)
    url = f"file://{dir_name}/index.html"
    webbrowser.open_new_tab(url)

    server_thread.join()

    # pip install gunicorn
    # gunicorn -w 4 -b 0.0.0.0:5000 app:app
