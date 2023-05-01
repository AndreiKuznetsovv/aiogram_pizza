import json

result = []

with open('cenz.txt', encoding='utf-8') as f_o:
    for line in f_o:
        word = line.strip().lower()
        if word != '':
            result.append(word)

with open('cenz.json', 'w', encoding='utf-8') as f_o:
    json.dump(result, f_o)