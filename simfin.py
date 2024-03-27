import json
import requests


class SimFin:
    def __init__(self, api_key):
        self.url = "https://backend.simfin.com/api/v3"
        self.api_key = api_key

    def _extract_financial_data(self, json_data):
        if not json_data or not json_data[0] or not json_data[0]["statements"]:
            raise Exception("No data found")
        data = json_data[0]["statements"][0]['data'][0]
        extracted_data = {}
        columns = json_data[0]["statements"][0]['columns']
        for index, key in enumerate(columns):
            extracted_data[key] = data[index]
        return extracted_data

    def _get_company_statements(self, ticker, statement, fyear, period):
        headers = {
            "Authorization": f"api-key {self.api_key}",
            "Accept": "application/json",
        }
        params = {
            "ticker": ticker,
            "statements": statement,
            "fyear": fyear,
            "period": period,
        }
        response = requests.get(f"{self.url}/companies/statements/compact", headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(
                f"Request failed with status code: {response.status_code}, response: {response.text}"
            )

        return response.json()

    def _build_summary_json(self, extracted_data, categories):
        summary_json = {}
        for category, keys in categories.items():
            summary_json[category] = {}
            for key in keys:
                value = extracted_data.get(key)
                if value is None:
                    formatted_value = "N/A"
                elif isinstance(value, (int, float)):
                    formatted_value = f"{value:,}"
                else:
                    formatted_value = value
                summary_json[category][key] = formatted_value
        return summary_json

    def get_derived(self, ticker, fyear, period):
        data = self._get_company_statements(ticker, "derived", fyear, period)
        extracted_data = self._extract_financial_data(data)
        column_map = {
            "Profitability Metrics": [
                "EBITDA",
                "Gross Profit Margin",
                "Operating Margin",
                "Net Profit Margin",
                "Return on Equity",
                "Return on Assets",
                "Return On Invested Capital",
            ],
            "Liquidity Metrics": ["Current Ratio"],
            "Solvency Metrics": [
                "Total Debt",
                "Liabilities to Equity Ratio",
                "Debt Ratio",
            ],
            "Cash Flow Metrics": [
                "Free Cash Flow",
                "Free Cash Flow to Net Income",
                "Cash Return On Invested Capital",
            ],
            "Other Important Metrics": [
                "Piotroski F-Score",
                "Net Debt / EBITDA",
                "Dividend Payout Ratio",
            ],
            "Metadata": ["Report Date"],
        }
        summary_json = self._build_summary_json(extracted_data, column_map)
        return summary_json

    def get_cash_flow(self, ticker, fyear, period):
        data = self._get_company_statements(ticker, "cf", fyear, period)
        extracted_data = self._extract_financial_data(data)
        column_map = {
            "Operating Activities": [
                "Change in Working Capital",
                "Net Cash from Operating Activities",
            ],
            "Investing Activities": [
                "Acquisition of Fixed Assets & Intangibles",
                "Net Cash from Investing Activities",
            ],
            "Financing Activities": [
                "Dividends Paid",
                "Cash from (Repayment of) Debt",
                "Net Cash from Financing Activities",
            ],
            "Net Change": ["Net Change in Cash"],
            "Metadata": ["Report Date", "Publish Date", "Source"],
        }
        summary_json = self._build_summary_json(extracted_data, column_map)
        return summary_json

    def get_profit_loss(self, ticker, fyear, period):
        data = self._get_company_statements(ticker, "pl", fyear, period)
        extracted_data = self._extract_financial_data(data)
        categories = {
            "Income": ["Revenue", "Gross Profit"],
            "Expenses": [
                "Operating Expenses",
            ],
            "Profitability": ["Operating Income (Loss)", "Pretax Income (Loss)"],
            "Metadata": ["Report Date", "Publish Date", "Source"],
        }
        summary_json = self._build_summary_json(extracted_data, categories)
        return summary_json

    def get_balance_sheet(self, ticker, fyear, period):
        data = self._get_company_statements(ticker, "bs", fyear, period)
        extracted_data = self._extract_financial_data(data)
        categories = {
            "Assets": [
                "Cash, Cash Equivalents & Short Term Investments",
                "Accounts & Notes Receivable",
                "Inventories",
                "Other Short Term Assets",
                "Total Current Assets",
                "Total Noncurrent Assets",
                "Total Assets",
            ],
            "Liabilities": [
                "Accounts Payable",
                "Short Term Debt",
                "Total Current Liabilities",
                "Long Term Debt",
                "Total Noncurrent Liabilities",
                "Total Liabilities",
            ],
            "Equity": [
                "Common Stock",
                "Retained Earnings",
                "Total Equity",
            ],
            "Summary": ["Total Liabilities & Equity"],
            "Metadata": ["Report Date", "Publish Date", "Source"],
        }
        summary_json = self._build_summary_json(extracted_data, categories)
        return summary_json

    def get_financials(self, ticker, fyear, period):
        balance_json = self.get_balance_sheet(ticker, fyear, period)
        cash_flow_json = self.get_cash_flow(ticker, fyear, period)
        derived_json = self.get_derived(ticker, fyear, period)
        profit_loss_json = self.get_profit_loss(ticker, fyear, period)
        return (
            balance_json,
            cash_flow_json,
            derived_json,
            profit_loss_json,
        )

    def get_financial_info_text(self, ticker: str, fyear: str, period: str):
        (
            balance_json,
            cash_flow_json,
            derived_json,
            profit_loss_json,
        ) = self.get_financials(ticker=ticker, fyear=fyear, period=period)
        return f"\
            {json.dumps(balance_json, indent=4)}\
            {json.dumps(cash_flow_json, indent=4)}\
            {json.dumps(derived_json, indent=4)}\
            {json.dumps(profit_loss_json, indent=4)}\
        "
