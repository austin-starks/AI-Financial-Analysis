import requests


class OpenAI:
    def __init__(self, api_key):
        self.api_key = api_key

    def chat(self, messages, func, model, temperature, message_limit):
        if not self.api_key:
            raise ValueError("API key for OpenAI is missing")

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        new_messages = messages[-message_limit:]
        data = {
            "model": model,
            "messages": new_messages,
            "temperature": temperature,
            "user": "self",
        }

        if func:
            data["functions"] = [func]
            data["function_call"] = {"name": func["name"]}

        response = requests.post(url, json=data, headers=headers)
        return response.json()
