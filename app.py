from flask import Flask, request, jsonify, redirect, send_file
from datetime import datetime, timedelta
import string
import random
import re
import os
from vercel_kv import VercelKV

app = Flask(__name__)

# Khởi tạo Vercel KV
kv = VercelKV()

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def is_valid_custom_code(code):
    return re.match(r'^[a-zA-Z0-9\-_]+$', code) is not None

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/shorten', methods=['POST'])
async def shorten_url():
    data = request.json
    original_url = data.get('url')
    custom_code = data.get('custom_code')

    if not original_url:
        return jsonify({"error": "Please enter a valid URL."}), 400

    if custom_code:
        if not is_valid_custom_code(custom_code):
            return jsonify({"error": "Invalid custom code. Use only letters, numbers, hyphens, and underscores."}), 400
        existing_url = await kv.get(f"url:{custom_code}")
        if existing_url:
            return jsonify({"error": "Custom code already in use. Please choose another."}), 400
        short_code = custom_code
    else:
        while True:
            short_code = generate_short_code()
            existing_url = await kv.get(f"url:{short_code}")
            if not existing_url:
                break

    await kv.set(f"url:{short_code}", {
        "original_url": original_url,
        "created_at": datetime.utcnow().isoformat(),
        "clicks": 0
    })
    return jsonify({"short_url": request.host_url + short_code, "original_url": original_url})

@app.route('/<short_code>')
async def redirect_to_url(short_code):
    url_data = await kv.get(f"url:{short_code}")
    if url_data:
        url_data['clicks'] += 1
        await kv.set(f"url:{short_code}", url_data)
        return redirect(url_data['original_url'])
    return "URL not found", 404

@app.route('/stats')
async def get_stats():
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    labels = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7, 0, -1)]
    clicks = [0] * 7
    
    async for key in kv.scan_iter("url:*"):
        url_data = await kv.get(key)
        created_at = datetime.fromisoformat(url_data['created_at'])
        if start_date <= created_at <= end_date:
            day_index = (end_date - created_at).days
            if 0 <= day_index < 7:
                clicks[6 - day_index] += url_data['clicks']
    
    return jsonify({"labels": labels, "clicks": clicks})

if __name__ == '__main__':
    app.run(debug=True)