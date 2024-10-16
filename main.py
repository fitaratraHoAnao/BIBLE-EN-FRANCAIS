from flask import Flask, jsonify
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/lire-la-bible', methods=['GET'])
def lire_la_bible():
    with open('/mnt/data/web.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

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

    def extract_books(section_heading):
        section = soup.find('h3', text=section_heading)
        books = []
        if section:
            book_list = section.find_next('ul', class_='list-group')
            books = [li.get_text(strip=True) for li in book_list.find_all('li')]
        return books

    # Ancien Testament
    bible_data["Ancien Testament"]["Le Pentateuque"] = extract_books("Le Pentateuque")
    bible_data["Ancien Testament"]["Livres historiques"] = extract_books("Livres historiques")
    bible_data["Ancien Testament"]["Livres poétiques"] = extract_books("Livres poétiques")
    bible_data["Ancien Testament"]["Les Prophètes"] = extract_books("Les Prophètes")

    # Nouveau Testament
    bible_data["Nouveau Testament"]["Les Evangiles"] = extract_books("Les Evangiles")
    bible_data["Nouveau Testament"]["Actes des Apôtres"] = extract_books("Actes des Apôtres")
    bible_data["Nouveau Testament"]["Epîtres de Paul"] = extract_books("Epîtres de Paul")
    bible_data["Nouveau Testament"]["Autres Epîtres"] = extract_books("Autres Epîtres")
    bible_data["Nouveau Testament"]["Livre de la Révélation"] = extract_books("Livre de la Révélation")

    return jsonify(bible_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
