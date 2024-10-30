from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/proxy', methods=['POST'])
def handle_post():
    try:
        data = request.json
        url = data['url']
        headers = data['headers']
        json_data = data['data']
    except (KeyError, TypeError):
        return jsonify({'error': 'Invalid input'}), 400

    response = requests.post(url, headers=headers, json=json_data)

    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
