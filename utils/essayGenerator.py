import requests 
import json 
import os 
import dotenv 

class EssayGenerator:
    def __init__(self, AI_KEY, AI_URL):
        self.AI_KEY = AI_KEY
        self.AI_URL = AI_URL                                                    
