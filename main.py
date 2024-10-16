import os
from flask import Flask, request, jsonify
from google.cloud import vision
from google.protobuf.json_format import MessageToDict
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API de Google Cloud Vision
api_key = os.getenv('API_CLOUD_VISION')

# Configurer la variable d'environnement pour l'API Cloud Vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key

app = Flask(__name__)

# Initialiser le client Cloud Vision
client = vision.ImageAnnotatorClient()

def load_image(image_data):
    """Charger une image envoyée via la requête POST."""
    return vision.Image(content=image_data)

@app.route('/object-detection', methods=['POST'])
def object_detection():
    """Route pour la reconnaissance d'objets."""
    image_file = request.files['image']
    image = load_image(image_file.read())
    response = client.object_localization(image=image)
    objects = MessageToDict(response._pb).get('localizedObjectAnnotations', [])
    return jsonify(objects)

@app.route('/text-detection', methods=['POST'])
def text_detection():
    """Route pour la détection de texte (OCR)."""
    image_file = request.files['image']
    image = load_image(image_file.read())
    response = client.text_detection(image=image)
    texts = MessageToDict(response._pb).get('textAnnotations', [])
    return jsonify(texts)

@app.route('/face-detection', methods=['POST'])
def face_detection():
    """Route pour la reconnaissance de visages."""
    image_file = request.files['image']
    image = load_image(image_file.read())
    response = client.face_detection(image=image)
    faces = MessageToDict(response._pb).get('faceAnnotations', [])
    return jsonify(faces)

@app.route('/label-detection', methods=['POST'])
def label_detection():
    """Route pour l'étiquetage d'images."""
    image_file = request.files['image']
    image = load_image(image_file.read())
    response = client.label_detection(image=image)
    labels = MessageToDict(response._pb).get('labelAnnotations', [])
    return jsonify(labels)

@app.route('/image-classification', methods=['POST'])
def image_classification():
    """Route pour la classification d'images."""
    image_file = request.files['image']
    image = load_image(image_file.read())
    response = client.label_detection(image=image)  # L'API utilise label_detection pour classifier les images.
    categories = MessageToDict(response._pb).get('labelAnnotations', [])
    return jsonify(categories)

@app.route('/safe-search-detection', methods=['POST'])
def safe_search_detection():
    """Route pour la détection de contenu explicite."""
    image_file = request.files['image']
    image = load_image(image_file.read())
    response = client.safe_search_detection(image=image)
    safe_search = MessageToDict(response._pb).get('safeSearchAnnotation', {})
    return jsonify(safe_search)

@app.route('/landmark-detection', methods=['POST'])
def landmark_detection():
    """Route pour la détection de points d'intérêt (Landmark)."""
    image_file = request.files['image']
    image = load_image(image_file.read())
    response = client.landmark_detection(image=image)
    landmarks = MessageToDict(response._pb).get('landmarkAnnotations', [])
    return jsonify(landmarks)

@app.route('/image-properties', methods=['POST'])
def image_properties():
    """Route pour l'analyse des couleurs et des propriétés d'images."""
    image_file = request.files['image']
    image = load_image(image_file.read())
    response = client.image_properties(image=image)
    properties = MessageToDict(response._pb).get('imagePropertiesAnnotation', {})
    return jsonify(properties)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
