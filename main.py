import os

from dotenv import load_dotenv
from pathlib import Path

import openai
import simfin

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)
simfin_token = os.environ["SIMFIN_TOKEN"]
openai_token = os.environ["OPENAI_API_KEY"]


def get_system_prompt():
    return """
    You are an AI Financial Analyst. Given company financials, you are asked to summarize the finances, 
    give pros and cons, and make a recommendation. You will explain the complex finances so that a 
    beginner without any financial knowledge can understand. You will always warn the user that they 
    need to do their own research, and that you are a guide to get started.
    """


def run(ticker: str, year: str, period: str):
    dats_wrangler = simfin.SimFin(simfin_token)
    content = dats_wrangler.get_financial_info_text(ticker, year, period)
    messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": content},
    ]
    for msg in messages[1:]:
        print(f"{msg['role'].capitalize()}\n", msg["content"], "\n")
    func = None
    model = "gpt-3.5-turbo"  # Replace with the model you want to use
    temperature = 0
    message_limit = 10  # Maximum number of messages to consider in the conversation
    client = openai.OpenAI(openai_token)
    response = client.chat(messages, func, model, temperature, message_limit)
    print("AI Assistant: ", response["choices"][0]["message"]["content"])


if __name__ == "__main__":
    run(ticker="AAPL", year="2023", period="Q1")
