from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import string
import random
import re
from datetime import datetime, timezone, timedelta
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Use the environment variable for the database URI
database_url = os.environ.get('DATABASE_URL', 'postgres://neondb_owner:npg_O2vKW0eoQulF@ep-dry-recipe-a1hoplhj-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require')

# If the URL starts with postgres://, replace it with postgresql://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Url(db.Model):
    __tablename__ = 'url'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    clicks = db.Column(db.Integer, default=0)

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def is_valid_custom_code(code):
    return re.match(r'^[a-zA-Z0-9-_]+$', code) is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    original_url = data.get('url')
    custom_code = data.get('custom_code')

    if not original_url:
        return jsonify({"error": "Please enter a valid URL."}), 400

    if custom_code:
        if not is_valid_custom_code(custom_code):
            return jsonify({"error": "Invalid custom code. Use only letters, numbers, hyphens, and underscores."}), 400
        existing_url = Url.query.filter_by(short_code=custom_code).first()
        if existing_url:
            return jsonify({"error": "Custom code already in use. Please choose another."}), 400
        short_code = custom_code
    else:
        while True:
            short_code = generate_short_code()
            existing_url = Url.query.filter_by(short_code=short_code).first()
            if not existing_url:
                break

    new_url = Url(original_url=original_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()
    return jsonify({"short_url": request.host_url + short_code, "original_url": original_url})

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url = Url.query.filter_by(short_code=short_code).first()
    if url:
        url.clicks += 1
        db.session.commit()
        return redirect(url.original_url)
    return "URL not found", 404

@app.route('/stats')
def get_stats():
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=7)
    
    urls = Url.query.filter(Url.created_at >= start_date).all()
    
    labels = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7, 0, -1)]
    clicks = [0] * 7
    
    for url in urls:
        day_index = (end_date - url.created_at).days
        if 0 <= day_index < 7:
            clicks[6 - day_index] += url.clicks
    
    return jsonify({"labels": labels, "clicks": clicks})

def init_db():
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

