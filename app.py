import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import traceback
from utils.essayGenerator import EssayGenerator
import flet as ft

load_dotenv()

AI_URL = os.getenv("AI_URL")
AI_KEY = os.getenv("AI_KEY")
AI_MODEL = os.getenv("AI_MODEL")

app = Flask(__name__)

EG = EssayGenerator(AI_KEY, AI_URL, AI_MODEL)

CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False
    }
})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route('/', methods=['GET'])
def home():
    return "Essay Generator API"

@app.route('/api/generate-essay', methods=['POST'])
def gennerate_essay():
    data = request.get_json()
    topic = data.get('topic')
    word_count = data.get('word_count', 500)
    extra_instructions = data.get('extra_instructions', '')

    if word_count != 500:
        try:
            word_count = int(word_count)
        except ValueError:
            return jsonify({"error": "Word count must be an integer"}), 400

        if word_count < 100:
            return jsonify({"error": "Word count must be at least 100"}), 400
        elif word_count > 1500:
            return jsonify({"error": "Word count must be at most 1500"}), 400
    
    if not topic:
        return jsonify({"error": "Topic is required"}), 400
        
    essay, error_msg = EG.generateEssay(topic,word_count,extra_instructions)

    if not essay or essay.strip() == "":
        if error_msg != "":
            return jsonify({"error": error_msg}), 500
        else:
            return jsonify({"error": "Unknown error occurred."}), 500
    
    return jsonify({"essay": essay}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)