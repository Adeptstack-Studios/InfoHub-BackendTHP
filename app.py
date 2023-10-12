from flask import Flask, jsonify, request
from json import dumps

app = Flask(__name__)


@app.route('/')
def welcome():
    return "<p>Hello API World!</p>"


@app.route('/js')
def send_json():
    file = open("ok.json")
    data = file.read()
    file.close()
    return data


@app.route('/json', methods=['POST'])
def receive_json():
    data = request.get_json()
    text = dumps(data)
    file = open("ok.json", "w")
    file.write(text)
    file.close()
    return text


if __name__ == '__main__':
    app.run()
