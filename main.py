import json
import os
import argparse

from dotenv import load_dotenv
from pathlib import Path

import openai
import simfin
from ollama import Ollama  # Assuming you've saved the Ollama class in a file named ollama.py

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)
SIMFIN_API_KEY = os.environ["SIMFIN_API_KEY"]
openai_token = os.environ.get("OPENAI_API_KEY")
ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434")


# Replace with the ticker, year, and period you want to analyze
ticker = "AAPL"
year = "2023"
period = "q1"


def get_system_prompt():
    return """
    You are an AI Financial Analyst. Given company financials, you are asked to summarize the finances, 
    give pros and cons, and make a recommendation. You will explain the complex finances so that a 
    beginner without any financial knowledge can understand. You will always warn the user that they 
    need to do their own research, and that you are a guide to get started.

    You will be given a JSON of financial data. You will restate the JSON in plain English,
    and then give the summary as described above. At the end of your message, you always cite any and all sources for the user. 
    Cite your sources in the format:
    For more detailed information, you can refer to the source provided:
    - Source Link 1
    - Source Link 2 (if applicable)
    """


def get_all_financial_data(ticker: str, year: str, period: str):
    dats_wrangler = simfin.SimFin(SIMFIN_API_KEY)
    (
        balance_json,
        cash_flow_json,
        derived_json,
        profit_loss_json,
    ) = dats_wrangler.get_financials(ticker, year, period)
    print("Balance Sheet\n", json.dumps(balance_json, indent=4), "\n")
    print("Cash Flow\n", json.dumps(cash_flow_json, indent=4), "\n")
    print("Derived\n", json.dumps(derived_json, indent=4), "\n")
    print("Profit Loss\n", json.dumps(profit_loss_json, indent=4), "\n")


def get_financial_data(ticker: str, year: str, period: str, statement: str):
    dats_wrangler = simfin.SimFin(SIMFIN_API_KEY)
    if statement == "bs":
        statement_json = dats_wrangler.get_balance_sheet(ticker, year, period)
    elif statement == "cf":
        statement_json = dats_wrangler.get_cash_flow(ticker, year, period)
    elif statement == "derived":
        statement_json = dats_wrangler.get_derived(ticker, year, period)
    elif statement == "pl":
        statement_json = dats_wrangler.get_profit_loss(ticker, year, period)
    else:
        raise ValueError("Statement must be one of bs, cf, derived, or pl")
    print("Balance Sheet\n", json.dumps(statement_json, indent=4), "\n")
    return statement_json


def get_financial_data_analysis(ticker: str, year: str, period: str, use_ollama: bool):
    dats_wrangler = simfin.SimFin(SIMFIN_API_KEY)
    content = dats_wrangler.get_financial_info_text(ticker, year, period)
    messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": content},
    ]

    if use_ollama:
        client = Ollama()
        model = "llama3.1"
    else:
        client = openai.OpenAI(api_key=openai_token)
        model = "gpt-4o-mini"

    temperature = 0
    response = client.chat(messages=messages, model=model, temperature=temperature)
    print(response)


def main():
    parser = argparse.ArgumentParser(description="Analyze financial data using AI")
    parser.add_argument("--use-ollama", action="store_true", help="Use Ollama instead of OpenAI")
    args = parser.parse_args()
    if not SIMFIN_API_KEY:
        raise ValueError("SIMFIN_API_KEY is not set")
    if args.use_ollama:
        return get_financial_data_analysis(ticker, year, period, use_ollama=True)
    
    if not openai_token:
        return get_all_financial_data(ticker, year, period)
    return get_financial_data_analysis(ticker, year, period, use_ollama=False)


if __name__ == "__main__":
    main()
