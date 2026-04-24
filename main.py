import requests
import json 
import os
from dotenv import load_dotenv

load_dotenv()

AI_URL = "https://ai.hackclub.com/proxy/v1/chat/completions"

AI_KEY = os.getenv("AI_KEY")



def answer(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AI_KEY}",
        "User-Agent": "Test_App",
    }

    payload = {
        "model": "google/gemini-3-flash-preview",
        "messages": [{ "role": "system", "content": "You are a helpful essay assistant. User is providing a topic for an essay. Respond with a well-structured (3-paragraph) essay with a proper introduction, body, and conclusion. Provide a short and straight forward topic (format topic given by user) as a markdown header." }, { "role": "user", "content": prompt }],
    }

    response = requests.post(AI_URL, json=payload, headers=headers)

    response = response.json()

    answer = response["choices"][0]["message"]["content"]

    return answer


if __name__ == "__main__":
    prompt = input("Tell the topic of essay: ")
    print(answer(prompt))
    