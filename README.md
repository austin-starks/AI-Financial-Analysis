# AI Financial Analyst

This script is an AI-powered financial analyst that summarizes company finances, provides pros and cons, and makes recommendations based on the provided financial information. It uses the OpenAI API or an open-source model from Ollama to generate the analysis.

[Video Demo of Applications of Large Language Models](https://www.youtube.com/watch?v=FW4WueDzxTI)

[Article on using LLMs for financial analysis and algorithmic trading](https://medium.com/p/146d67c52cdb)

## Check out NexusTrade

For a fully functional platform, [check out NexusTrade](https://nexustrade.io/). NexusTrade is a AI-Powered automated trading and investment platform that allows users to create, test, optimize, and deploy algorithmic trading strategies. It's fast, configurable, easy to use, and requires no code!

NexusTrade has this feature implemented in it's [AI-Powered Chat](https://nexustrade.io/chat). It requires no setup and it's easy for everybody, even non-developers, to use. Just create an account and try it out.

## Installation

To run the script, you need to have the following packages installed:

- requests==2.26.0
- python-dotenv==0.19.1

You can install these packages by running the following command:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Before running the script, you need to set up your environment variables. Create a `.env` file in the project directory and add the following variables:

```plaintext
SIMFIN_API_KEY=YOUR_SIMFIN_API_KEY
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

Replace `YOUR_SIMFIN_API_KEY` with your SimFin API token and `YOUR_OPENAI_API_KEY` with your OpenAI API key.

## Setting Up Ollama

To use Ollama as an alternative to OpenAI, follow these steps:

1. **Download Ollama**: Go to [ollama.com/download](https://ollama.com/download) and download the appropriate version for your operating system.

2. **Download the Model**: Visit [ollama.com/library/llama3.1](https://ollama.com/library/llama3.1) to download the model you want to use.

3. **(Optional) Set the Environment Variable**: If Ollama is not running on the default port, you must set up the following environment variable in your `.env` file:

```plaintext
OLLAMA_SERVICE_URL=http://localhost:11434
```

## Usage

To use the AI Financial Analyst with OpenAI, run the following command:

```
python chat.py
```

To use it with Ollama, run this command instead:

```
python chat.py --use-ollama
```

The script will provide a summary of the company's finances based on the provided financial information. It will analyze the balance sheet, cash flow, profitability metrics, liquidity metrics, solvency metrics, cash flow metrics, and other important metrics. The script will also provide a recommendation based on the analysis.

## Output

Here is an example output from running the script on Apple for Q1 2023:

```
AI Assistant:  Based on the provided financial information, here is a summary of the company's finances:

1. Balance Sheet:
   - Total Assets: $346,747,000,000
   - Total Liabilities: $290,020,000,000
   - Total Equity: $56,727,000,000

   The company has a strong balance sheet with a significant amount of assets compared to its liabilities. This indicates a healthy financial position.

2. Cash Flow:
   - Net Cash from Operating Activities: $34,005,000,000
   - Net Cash from Investing Activities: -$1,445,000,000
   - Net Cash from Financing Activities: -$35,563,000,000
   - Net Change in Cash: -$3,003,000,000

   The company generated positive cash flow from its operating activities, but had negative cash flow from investing and financing activities. As a result, there was a decrease in cash during the period.

3. Profitability Metrics:
   - Gross Profit Margin: 42.96%
   - Operating Margin: 30.74%
   - Net Profit Margin: 25.61%
   - Return on Equity: 52.88%
   - Return on Assets: 8.65%
   - Return on Invested Capital: 15.28%

   The company has healthy profitability metrics, indicating efficient operations and good returns on investment.

4. Liquidity Metrics:
   - Current Ratio: 1.01

   The company has a current ratio slightly above 1, which suggests it has enough current assets to cover its short-term liabilities. However, it is important to note that a current ratio of exactly 1 may indicate limited liquidity.

5. Solvency Metrics:
   - Liabilities to Equity Ratio: 5.11
   - Debt Ratio: 32.04%

   The company has a relatively high liabilities to equity ratio, indicating a significant amount of debt compared to equity. The debt ratio is moderate, suggesting that a significant portion of the company's assets is financed by debt.

6. Cash Flow Metrics:
   - Free Cash Flow: $39,273,000,000
   - Free Cash Flow to Net Income: 1.31
   - Cash Return on Invested Capital: 17.77%

   The company has positive free cash flow, indicating its ability to generate cash after accounting for capital expenditures. The free cash flow to net income ratio suggests that the company is efficient in converting its net income into free cash flow. The cash return on invested capital is also positive, indicating good returns on the capital invested.

7. Other Important Metrics:
   - Piotroski F-Score: 4
   - Net Debt / EBITDA: 1.53
   - Dividend Payout Ratio: 12.56%

   The Piotroski F-Score of 4 suggests that the company has a moderate financial strength. The net debt to EBITDA ratio indicates the company's ability to repay its debt, with a ratio of 1.53. The dividend payout ratio suggests that the company distributes a portion of its earnings as dividends.

Based on the provided information, the company appears to be in a strong financial position with healthy profitability metrics and positive cash flow. However, it is important to conduct further research and analysis to fully understand the company's financial health and prospects.
```

## Attribution

This script utilizes the SimFin API for retrieving company financial information and the OpenAI API for generating the AI analysis.

## Disclaimer

Please note that this script should be used as a starting point and not as financial advice. It is important to conduct further research and analysis before making any investment decisions.
