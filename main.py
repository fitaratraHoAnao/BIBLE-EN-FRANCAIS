from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Route pour lire la structure de la Bible (Ancien et Nouveau Testament)
@app.route('/lire-la-bible', methods=['GET'])
def lire_la_bible():
    # URL de la page à scraper
    url = "https://emcitv.com/bible/lire-la-bible.html"
    
    # Effectuer une requête pour obtenir la page HTML
    response = requests.get(url)
    
    # Parser le HTML avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialiser le dictionnaire qui contiendra les sections de la Bible
    bible_data = {
        "Ancien Testament": {
            "Le Pentateuque": [],
            "Livres historiques": [],
            "Livres poétiques": [],
            "Les Prophètes": []
        },
        "Nouveau Testament": {
            "Les Evangiles": [],
            "Actes des Apôtres": [],
            "Epîtres de Paul": [],
            "Autres Epîtres": [],
            "Livre de la Révélation": []
        }
    }

    # Fonction pour scraper une section spécifique de livres bibliques
    def extract_books(section_title):
        section = soup.find('h3', string=section_title)
        books = []
        if section:
            # Trouver tous les livres dans la section
            book_list = section.find_next('ul', class_='list-group')
            if book_list:
                books = [li.get_text(strip=True) for li in book_list.find_all('li')]
            else:
                print(f"Aucune liste de livres trouvée pour {section_title}")
        else:
            print(f"Section non trouvée : {section_title}")
        return books

    # Scraper chaque partie de l'Ancien Testament
    bible_data["Ancien Testament"]["Le Pentateuque"] = extract_books("Le Pentateuque")
    bible_data["Ancien Testament"]["Livres historiques"] = extract_books("Livres historiques")
    bible_data["Ancien Testament"]["Livres poétiques"] = extract_books("Livres poétiques")
    bible_data["Ancien Testament"]["Les Prophètes"] = extract_books("Les Prophètes")

    # Scraper chaque partie du Nouveau Testament
    bible_data["Nouveau Testament"]["Les Evangiles"] = extract_books("Les Evangiles")
    bible_data["Nouveau Testament"]["Actes des Apôtres"] = extract_books("Actes des Apôtres")
    bible_data["Nouveau Testament"]["Epîtres de Paul"] = extract_books("Epîtres de Paul")
    bible_data["Nouveau Testament"]["Autres Epîtres"] = extract_books("Autres Epîtres")
    
    # Ajout explicite pour le livre Apocalypse
    bible_data["Nouveau Testament"]["Livre de la Révélation"] = extract_books("Livre de la Révélation") + ["Apocalypse"]

    # Retourner les résultats sous forme de JSON
    return jsonify(bible_data)

# Route pour rechercher un livre et un chapitre spécifique
@app.route('/recherche', methods=['GET'])
def recherche_bible():
    # Récupérer les paramètres de l'URL
    livre = request.args.get('bible', 'genese').lower()
    chapitre = request.args.get('chapitre', '1')

    # Construire l'URL de la page à scraper
    base_url = f"https://emcitv.com/bible/{livre}.html"
    if chapitre != '1':
        base_url = f"https://emcitv.com/bible/{livre}-{chapitre}.html"

    # Effectuer la requête HTTP pour obtenir le contenu de la page
    response = requests.get(base_url)
    
    if response.status_code != 200:
        return jsonify({"error": "Page non trouvée"}), 404

    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraire le nom du livre et du chapitre
    titre_livre = soup.find('h1', class_='book').text.strip()
    titre_chapitre = soup.find('span', class_='label-chapters').text.strip()

    # Extraire les versets du chapitre
    versets = []
    for verse in soup.find_all('span', class_='verse'):
        num = verse.find('a', class_='num').text.strip()
        contenu = verse.find('span', class_='content').text.strip()
        versets.append(f"{num} {contenu}")

    # Créer le dictionnaire de résultat
    result = {
        "livre": titre_livre,
        "chapitre": titre_chapitre,
        "versets": versets
    }

    # Retourner les résultats sous forme de JSON
    return jsonify(result)

# Nouvelle route pour rechercher un verset spécifique
@app.route('/verser', methods=['GET'])
def chercher_verser():
    # Récupérer le paramètre 'question' dans l'URL
    question = request.args.get('question', '').lower()
    
    if not question:
        return jsonify({"error": "Vous devez fournir une question."}), 400

    # Séparer le livre et les versets dans la question (par exemple 'genese 15-18')
    try:
        parts = question.split()
        livre = parts[0]
        versets = parts[1]
        chapitre, debut_fin = versets.split('-')
    except (IndexError, ValueError):
        return jsonify({"error": "Format incorrect. Utilisez 'livre chapitre-début_fin', par exemple 'genese 15-18'."}), 400

    # Construire l'URL de la page à scraper
    base_url = f"https://emcitv.com/bible/{livre}.html"
    if chapitre != '1':
        base_url = f"https://emcitv.com/bible/{livre}-{chapitre}.html"

    # Effectuer la requête HTTP pour obtenir le contenu de la page
    response = requests.get(base_url)
    if response.status_code != 200:
        return jsonify({"error": "Page non trouvée"}), 404

    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraire les versets du chapitre
    versets_extraits = []
    for verse in soup.find_all('span', class_='verse'):
        num = verse.find('a', class_='num').text.strip()
        contenu = verse.find('span', class_='content').text.strip()
        if int(debut_fin.split('-')[0]) <= int(num) <= int(debut_fin.split('-')[1]):
            versets_extraits.append(f"{num} {contenu}")

    # Si aucun verset n'est trouvé
    if not versets_extraits:
        return jsonify({"error": "Aucun verset trouvé dans la plage spécifiée."}), 404

    # Créer la réponse au format JSON
    resultat = {
        "question": question,
        "versets": versets_extraits
    }

    # Retourner les résultats sous forme de JSON
    return jsonify(resultat)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
