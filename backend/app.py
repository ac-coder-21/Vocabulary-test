from flask import Flask, request, jsonify
from flask_cors import CORS
import json, random


app = Flask(__name__)
CORS(app=app)

@app.get('/')
def get_learn_data():
    with open("./data/json/A1_Nouns.json", 'r', encoding='utf-8') as noun_file:
        nouns = json.load(noun_file)

    with open("./data/json/A1_Verbs.json", 'r', encoding='utf-8') as verb_file:
            verbs = json.load(verb_file)

    with open("./data/json/A1_Adjectives.json", 'r', encoding='utf-8') as adjective_file:
            adjectives = json.load(adjective_file)

    with open('./data/json/A1_Others.json', 'r', encoding='utf-8') as other_file:
            others = json.load(other_file)
    
    number_of_words_learned = (len(nouns['words']) + len(verbs['words']) + len(adjectives['words']) + len(others['words'])) 

    return { "home_data": [number_of_words_learned]}

@app.get('/test')
def get_random_german_word():
    file_name = request.args.get('file')
    if not file_name:
        return jsonify({"error": "No file specified"}), 400
    
    file_name = file_name.replace(' ', '_')


    with open(f'./data/json/{file_name}.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    words = data.get("words", [])
    if words:
        random.shuffle(words)
        response = jsonify(words)
        response.headers.add('Content-Type', 'application/json; charset=utf-8')
        return response
    else:
        return jsonify({"error": "No words available"}), 404

if __name__ == '__main__':
    app.run(debug=True)
