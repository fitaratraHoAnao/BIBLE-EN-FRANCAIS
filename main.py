from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/lire-la-bible', methods=['GET'])
def lire_la_bible():
    url = "https://emcitv.com/bible/lire-la-bible.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Scraping des livres
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

    # Ancien Testament
    ancien_testament_sections = soup.select('div.col-md-6 h2:contains("Ancien testament") + div.panel')
    for section in ancien_testament_sections:
        section_title = section.select_one('.panel-title').text.strip()
        books = [li.text.strip() for li in section.select('.list-group-item')]
        if "Pentateuque" in section_title:
            bible_data["Ancien Testament"]["Le Pentateuque"].extend(books)
        elif "historiques" in section_title:
            bible_data["Ancien Testament"]["Livres historiques"].extend(books)
        elif "poétiques" in section_title:
            bible_data["Ancien Testament"]["Livres poétiques"].extend(books)
        elif "Prophètes" in section_title:
            bible_data["Ancien Testament"]["Les Prophètes"].extend(books)

    # Nouveau Testament
    nouveau_testament_sections = soup.select('div.col-md-6 h2:contains("Nouveau testament") + div.panel')
    for section in nouveau_testament_sections:
        section_title = section.select_one('.panel-title').text.strip()
        books = [li.text.strip() for li in section.select('.list-group-item')]
        if "Evangiles" in section_title:
            bible_data["Nouveau Testament"]["Les Evangiles"].extend(books)
        elif "Actes des Apôtres" in section_title:
            bible_data["Nouveau Testament"]["Actes des Apôtres"].extend(books)
        elif "Epîtres de Paul" in section_title:
            bible_data["Nouveau Testament"]["Epîtres de Paul"].extend(books)
        elif "Autres Epîtres" in section_title:
            bible_data["Nouveau Testament"]["Autres Epîtres"].extend(books)
        elif "Révélation" in section_title:
            bible_data["Nouveau Testament"]["Livre de la Révélation"].extend(books)

    return jsonify(bible_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        
