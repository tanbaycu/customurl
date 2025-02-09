from flask import Flask, request, jsonify, redirect, send_file
from datetime import datetime, timedelta
import string
import random
import re
import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

EDGE_CONFIG_ID = os.getenv('EDGE_CONFIG_ID')
EDGE_CONFIG_TOKEN = os.getenv('EDGE_CONFIG_TOKEN')

async def edge_config_get(key):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://edge-config.vercel.com/v1/items/{key}",
            headers={
                "Authorization": f"Bearer {EDGE_CONFIG_TOKEN}",
                "Content-Type": "application/json",
            },
        )
        if response.status_code == 200:
            return response.json()
        return None

async def edge_config_set(key, value):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"https://edge-config.vercel.com/v1/items/{key}",
            headers={
                "Authorization": f"Bearer {EDGE_CONFIG_TOKEN}",
                "Content-Type": "application/json",
            },
            json={"value": value},
        )
        return response.status_code == 200

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def is_valid_custom_code(code):
    return re.match(r'^[a-zA-Z0-9\-_]+$', code) is not None

@app.route('/')
def index():
    return send_file('templates/index.html')

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
        existing_url = await edge_config_get(f"url:{custom_code}")
        if existing_url:
            return jsonify({"error": "Custom code already in use. Please choose another."}), 400
        short_code = custom_code
    else:
        while True:
            short_code = generate_short_code()
            existing_url = await edge_config_get(f"url:{short_code}")
            if not existing_url:
                break

    await edge_config_set(f"url:{short_code}", original_url)
    await edge_config_set(f"stats:{short_code}", json.dumps({
        "created_at": datetime.utcnow().isoformat(),
        "clicks": 0
    }))
    return jsonify({"short_url": request.host_url + short_code, "original_url": original_url})

@app.route('/<short_code>')
async def redirect_to_url(short_code):
    original_url = await edge_config_get(f"url:{short_code}")
    if original_url:
        stats = json.loads(await edge_config_get(f"stats:{short_code}") or '{}')
        stats['clicks'] = stats.get('clicks', 0) + 1
        await edge_config_set(f"stats:{short_code}", json.dumps(stats))
        return redirect(original_url)
    return "URL not found", 404

@app.route('/stats')
async def get_stats():
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    labels = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7, 0, -1)]
    clicks = [0] * 7
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://edge-config.vercel.com/v1/items",
            headers={
                "Authorization": f"Bearer {EDGE_CONFIG_TOKEN}",
                "Content-Type": "application/json",
            },
        )
        if response.status_code == 200:
            all_items = response.json()
            for key, value in all_items.items():
                if key.startswith("stats:"):
                    stats = json.loads(value)
                    created_at = datetime.fromisoformat(stats['created_at'])
                    if start_date <= created_at <= end_date:
                        day_index = (end_date - created_at).days
                        if 0 <= day_index < 7:
                            clicks[6 - day_index] += stats['clicks']
    
    return jsonify({"labels": labels, "clicks": clicks})

if __name__ == '__main__':
    app.run(debug=True)