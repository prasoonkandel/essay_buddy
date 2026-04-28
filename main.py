import os
from dotenv import load_dotenv
from utils.essayGenerator import EssayGenerator

load_dotenv()

AI_URL = "https://ai.hackclub.com/proxy/v1/chat/completions"
AI_KEY = os.getenv("AI_KEY")
MODEL = "google/gemini-3-flash-preview"

if not AI_KEY:
    raise ValueError("AI_KEY not found in environment variables")

eg = EssayGenerator(AI_KEY, AI_URL, MODEL)

if __name__ == "__main__":
    topic = input("Enter the topic for the essay: ")
    extra_instructions = input("Provide additional instruction: ")
    word_count = input("Enter the desired word count for the essay (default is 500): ")
    if word_count.strip() == "":
        word_count = 500
    else:
        try:
            word_count = int(word_count)
        except ValueError:
            print("Invalid input for word count. Using default value of 500.")
            word_count = 500
    essay = eg.generateEssay(topic, extra_instructions, word_count)
    print(essay)

