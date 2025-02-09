from flask import Flask, request, jsonify, redirect, send_file
from datetime import datetime, timedelta
import string
import random
import re
import requests
import os
import json

app = Flask(__name__)

# JSONbin setup
JSONBIN_API_KEY = os.environ.get('JSONBIN_API_KEY')
JSONBIN_BIN_ID = os.environ.get('JSONBIN_BIN_ID')
JSONBIN_URL = f"https://api.jsonbin.io/v3/b/{JSONBIN_BIN_ID}"

headers = {
    "Content-Type": "application/json",
    "X-Master-Key": JSONBIN_API_KEY
}

# Helper functions
def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def is_valid_custom_code(code):
    return re.match(r'^[a-zA-Z0-9\-_]+$', code) is not None

def get_jsonbin_data():
    response = requests.get(JSONBIN_URL, headers=headers)
    if response.status_code == 200:
        return response.json()['record']
    return {'urls': []}

def update_jsonbin_data(data):
    response = requests.put(JSONBIN_URL, json=data, headers=headers)
    return response.status_code == 200

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    original_url = data.get('url')
    custom_code = data.get('custom_code')

    if not original_url:
        return jsonify({"error": "Please enter a valid URL."}), 400

    jsonbin_data = get_jsonbin_data()

    if custom_code:
        if not is_valid_custom_code(custom_code):
            return jsonify({"error": "Invalid custom code. Use only letters, numbers, hyphens, and underscores."}), 400
        if any(url['short_code'] == custom_code for url in jsonbin_data['urls']):
            return jsonify({"error": "Custom code already in use. Please choose another."}), 400
        short_code = custom_code
    else:
        while True:
            short_code = generate_short_code()
            if not any(url['short_code'] == short_code for url in jsonbin_data['urls']):
                break

    new_url = {
        "original_url": original_url,
        "short_code": short_code,
        "created_at": datetime.utcnow().isoformat(),
        "clicks": 0
    }

    jsonbin_data['urls'].append(new_url)
    if update_jsonbin_data(jsonbin_data):
        return jsonify({"short_url": request.host_url + short_code, "original_url": original_url})
    else:
        return jsonify({"error": "Failed to create short URL. Please try again."}), 500

@app.route('/<short_code>')
def redirect_to_url(short_code):
    jsonbin_data = get_jsonbin_data()
    for url in jsonbin_data['urls']:
        if url['short_code'] == short_code:
            url['clicks'] += 1
            update_jsonbin_data(jsonbin_data)
            return redirect(url['original_url'])
    return "URL not found", 404

@app.route('/stats')
def get_stats():
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    labels = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7, 0, -1)]
    
    jsonbin_data = get_jsonbin_data()
    clicks = [0] * 7

    for url in jsonbin_data['urls']:
        created_at = datetime.fromisoformat(url['created_at'])
        if start_date <= created_at <= end_date:
            day_index = (end_date.date() - created_at.date()).days
            if 0 <= day_index < 7:
                clicks[day_index] += url['clicks']

    return jsonify({"labels": labels, "clicks": clicks[::-1]})

if __name__ == '__main__':
    app.run(debug=True)