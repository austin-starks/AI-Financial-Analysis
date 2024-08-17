import os
import json
from dotenv import load_dotenv
from pathlib import Path
from main import get_financial_data_analysis, get_all_financial_data
import openai
from datetime import datetime

# Load environment variables
dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)
simfin_token = os.environ["SIMFIN_TOKEN"]
openai_token = os.environ.get("OPENAI_API_KEY")

def get_system_prompt():
    prompt = """
    You are a chat application that will help users analyze financial data.

    You need the 3 following inputs:
    - Stock ticker symbol
    - Year (e.g., 2023)
    - Period (q1, q2, q3, q4, fy)

    Have a conversation with the user to get these inputs. During each iteration, you are going to iteratively build the JSON object with the necessary information.
    
    Once you have everything, thank the user and tell them to give you a moment to analyze the data.

    ##REMEMBER##
    * Convert stock names (e.g. "Apple", "Amazon", or "Google") to their respective ticker symbols (AAPL, AMZN, GOOG).
    * Google and GOOGL must be converted to GOOG
    * Facebook and FB must be converted to META
    * You MUST generate a syntactically correct JSON object

    ##OUTPUT FORMAT##
    Each response MUST be a syntactically correct JSON with the following format:
    {
        "message": string,
        "data": {
            "ticker": string | null
            "year": int | null
            "period": string | null
        }
    }
    """
    return f"{prompt}\nToday's date is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."

def chat_with_user():
    print("Hi! I'm an AI that helps you perform financial analysis.")
    print("What stock do you want to analyze? For example, you can say 'I'm interested in AAPL'.")
    # Initialize the conversation with the system prompt
    messages = [{"role": "system", "content": get_system_prompt()}]
     # Ask the user for the stock ticker
    user_input = input().strip()
    messages.append({"role": "user", "content": user_input})
    while True:
        # Call the OpenAI API to validate the ticker and get more info
        model = "gpt-4o-mini"  # Replace with the model you want to use
        temperature = 0
        client = openai.OpenAI(openai_token)
        response = client.chat(messages, model, temperature)

        # Add the LLM's response to the conversation history
        messages.append({"role": "assistant", "content": response})

        # Check if the response includes a JSON and try to parse it
        if "{" in response and "}" in response:
            try:
                json_str = response[response.index("{"):response.rindex("}")+1]
                data = json.loads(json_str)
                
                # Extract necessary fields
                ticker = data.get("data").get("ticker")
                year = data.get("data").get("year")
                period = data.get("data").get("period")

                # Validate that necessary information is available
                if ticker and year and period:
                    print(data.get("message"))
                    # Use the functions from main.py to perform the analysis
                    get_financial_data_analysis(ticker, year, period)
                    response = input("\nWould you like to analyze another stock? Press Enter to continue or type 'exit' to quit.\n")
                    if response.lower() == "exit":
                        print("Thank you for using the AI assistant. Goodbye!")
                        break
                    else:
                        messages.append({"role": "user", "content": "The user wants to analyze another stock."})

                else:
                    user_response = input(f"{data.get("message")}\n").strip()
                    messages.append({"role": "user", "content": user_response})
            except json.JSONDecodeError:
                print(response)
                print("Oops! I broke. Sorry about that!")
        else:
            print(response)
            print("Oops! I broke. Sorry about that!")
            messages.append({"role": "user", "content": "Remember, you MUST generate a syntactically correct JSON object."})



if __name__ == "__main__":
    chat_with_user()
