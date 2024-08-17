import requests


class OpenAI:
    def __init__(self, api_key):
        self.api_key = api_key

    def chat(self, messages, model, temperature):
        if not self.api_key:
            raise ValueError("API key for OpenAI is missing")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "user": "self",
        }

        response = requests.post(url, json=data, headers=headers)
        return response.json()["choices"][0]["message"]["content"]
