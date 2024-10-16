import os
from flask import Flask, request, jsonify
import requests
import base64
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env (si nécessaire)
load_dotenv()

# Utiliser la clé API fournie directement dans les requêtes
API_KEY = 'API_CLOUD_VISION'

app = Flask(__name__)

def call_vision_api(features, image_content):
    """Appelle l'API Google Cloud Vision pour effectuer des analyses d'images."""
    endpoint = f'https://vision.googleapis.com/v1/images:annotate?key={API_KEY}'
    headers = {'Content-Type': 'application/json'}
    
    # Requête JSON envoyée à l'API Vision
    body = {
        'requests': [{
            'image': {'content': image_content},
            'features': features
        }]
    }
    
    response = requests.post(endpoint, json=body, headers=headers)
    return response.json()

def encode_image(image):
    """Encode une image en base64."""
    return base64.b64encode(image).decode('utf-8')

@app.route('/object-detection', methods=['POST'])
def object_detection():
    """Route pour la reconnaissance d'objets."""
    image_file = request.files['image']
    image_content = encode_image(image_file.read())
    features = [{'type': 'OBJECT_LOCALIZATION'}]
    
    result = call_vision_api(features, image_content)
    return jsonify(result)

@app.route('/text-detection', methods=['POST'])
def text_detection():
    """Route pour la détection de texte (OCR)."""
    image_file = request.files['image']
    image_content = encode_image(image_file.read())
    features = [{'type': 'TEXT_DETECTION'}]
    
    result = call_vision_api(features, image_content)
    return jsonify(result)

@app.route('/face-detection', methods=['POST'])
def face_detection():
    """Route pour la reconnaissance de visages."""
    image_file = request.files['image']
    image_content = encode_image(image_file.read())
    features = [{'type': 'FACE_DETECTION'}]
    
    result = call_vision_api(features, image_content)
    return jsonify(result)

@app.route('/label-detection', methods=['POST'])
def label_detection():
    """Route pour l'étiquetage d'images."""
    image_file = request.files['image']
    image_content = encode_image(image_file.read())
    features = [{'type': 'LABEL_DETECTION'}]
    
    result = call_vision_api(features, image_content)
    return jsonify(result)

@app.route('/image-classification', methods=['POST'])
def image_classification():
    """Route pour la classification d'images."""
    image_file = request.files['image']
    image_content = encode_image(image_file.read())
    features = [{'type': 'LABEL_DETECTION'}]
    
    result = call_vision_api(features, image_content)
    return jsonify(result)

@app.route('/safe-search-detection', methods=['POST'])
def safe_search_detection():
    """Route pour la détection de contenu explicite."""
    image_file = request.files['image']
    image_content = encode_image(image_file.read())
    features = [{'type': 'SAFE_SEARCH_DETECTION'}]
    
    result = call_vision_api(features, image_content)
    return jsonify(result)

@app.route('/landmark-detection', methods=['POST'])
def landmark_detection():
    """Route pour la détection de points d'intérêt (Landmark)."""
    image_file = request.files['image']
    image_content = encode_image(image_file.read())
    features = [{'type': 'LANDMARK_DETECTION'}]
    
    result = call_vision_api(features, image_content)
    return jsonify(result)

@app.route('/image-properties', methods=['POST'])
def image_properties():
    """Route pour l'analyse des couleurs et des propriétés d'images."""
    image_file = request.files['image']
    image_content = encode_image(image_file.read())
    features = [{'type': 'IMAGE_PROPERTIES'}]
    
    result = call_vision_api(features, image_content)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
