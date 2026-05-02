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