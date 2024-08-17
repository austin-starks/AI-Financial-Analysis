import json
import os

from dotenv import load_dotenv
from pathlib import Path

import openai
import simfin

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)
simfin_token = os.environ["SIMFIN_TOKEN"]
openai_token = os.environ.get("OPENAI_API_KEY")

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
    dats_wrangler = simfin.SimFin(simfin_token)
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
    dats_wrangler = simfin.SimFin(simfin_token)
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


def get_financial_data_analysis(ticker: str, year: str, period: str):
    dats_wrangler = simfin.SimFin(simfin_token)
    content = dats_wrangler.get_financial_info_text(ticker, year, period)
    messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": content},
    ]
    model = "gpt-4o-mini"  # Replace with the model you want to use
    temperature = 0
    client = openai.OpenAI(openai_token)
    response = client.chat(messages, model, temperature)
    print(response)


def main():
    if not simfin_token:
        raise ValueError("SIMFIN_TOKEN is not set")
    if not openai_token:
        return get_all_financial_data(ticker, year, period)
    return get_financial_data_analysis(ticker, year, period)


if __name__ == "__main__":
    main()
