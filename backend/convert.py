import pandas as pd
import json
from flask import jsonify

class GermanCharEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, str):
            return obj.encode('utf-8').decode('utf-8')
        return super().default(obj)

def convert_json(german_words, english_words, file_name):
    try:
        with open(f'./data/json/{file_name}.json', 'r+', encoding='utf-8') as file:
            file_data = json.load(file)
            file_data['words'].clear()
            for word_index in range(len(german_words)):
                file_data['words'].append({"german": german_words[word_index], "english": english_words[word_index]})
            file.seek(0)
            json.dump(file_data, file, indent=4, ensure_ascii=False, cls=GermanCharEncoder)
            file.truncate()
        
        return jsonify("Data converted successfully"), 200
    except FileNotFoundError:
        return jsonify("File not found for conversion"), 404

def main():
    file_name = input("Enter File Name: ")

    data = pd.read_csv(f'./data/csv/{file_name}.csv', encoding='utf-8')

    german_words = data['German'].tolist()
    english_words = data['English'].tolist()

    result = convert_json(german_words=german_words, english_words=english_words, file_name=file_name)
    print(result.get_data(as_text=True))

if __name__ == "__main__":
    main()