import requests
import base64

class Ollama:
    def __init__(self):
        self.base_url = "http://localhost:11434"

    def chat(self, messages, model, temperature=0.0):
        url = f"{self.base_url}/api/chat"
        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()["message"]['content']

    def embeddings(self, prompt):
        url = f"{self.base_url}/api/embeddings"
        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "prompt": prompt,
            "model": "nomic-embed-text",
        }

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()["embedding"]

    def analyze_image(self, image_path, model, prompt):
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")

        url = f"{self.base_url}/api/generate"
        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "model": model,
            "prompt": prompt,
            "images": [base64_image],
            "stream": False,
        }

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()["response"]
