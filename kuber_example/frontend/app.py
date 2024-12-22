import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

BACKEND_URL = os.getenv('BACKEND_URL')


@app.route('/api/classifier/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    response = requests.post(BACKEND_URL + '/api/classifier/analyze', json=data)

    try:
        response_json = response.json()
    except ValueError:
        return jsonify({"error": "Invalid or empty response from backend"}), 500

    return jsonify(response_json), response.status_code


@app.route('/api/classifier/analyze_status/<id_>', methods=['GET'])
def analyze_status(id_):
    response = requests.get(BACKEND_URL + f'/api/classifier/analyze_status/{id_}')
    try:
        response_json = response.json()
    except ValueError:
        return jsonify({"error": "Invalid or empty response from backend"}), 500

    return jsonify(response_json), response.status_code


@app.route('/api/classifier/get_result/<id_>', methods=['GET'])
def get_result(id_):
    response = requests.get(BACKEND_URL + f'/api/classifier/get_result/{id_}')
    try:
        response_json = response.json()
    except ValueError:
        return jsonify({"error": "Invalid or empty response from backend"}), 500

    return jsonify(response_json), response.status_code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9994)