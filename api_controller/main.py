from flask import Flask
import os
import json

app = Flask(__name__)

DATA_DIRECTORY = '/app/data'

@app.route('/list')
def get_list():
    datasets = {}

    for filename in os.listdir(DATA_DIRECTORY):
        with open(f"{DATA_DIRECTORY}/{filename}", 'r') as f:
            data = json.load(f)
        datasets[os.path.splitext(filename)[0]] = data

    items = []
    for dataset in datasets:
        for key in datasets[dataset]:
            items.append(key)

    return json.dumps(items)

@app.route('/item/<code>')
def get_item(code):
    datasets = {}

    for filename in os.listdir(DATA_DIRECTORY):
        with open(f"{DATA_DIRECTORY}/{filename}", 'r') as f:
            data = json.load(f)
        datasets[os.path.splitext(filename)[0]] = data

    for dataset in datasets:
        for key in datasets[dataset]:
            if (key == code):
                return json.dumps({key: datasets[dataset][key]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)