import json
import requests


class SimFin:
    def __init__(self, api_key):
        self.url = "https://simfin.com/api/v2/"
        self.api_key = api_key

    def _extract_financial_data(self, json_data, column_map):
        if not json_data or not json_data[0] or not json_data[0]["found"]:
            raise Exception("No data found")
        financial_data = json_data[0]["data"][0]
        extracted_data = {}

        for key, index in column_map.items():
            extracted_data[key] = financial_data[index]

        return extracted_data

    def _get_company_statements(self, ticker, statement, fyear, period):
        params = {
            "api-key": self.api_key,
            "ticker": ticker,
            "statement": statement,
            "fyear": fyear,
            "period": period,
        }
        response = requests.get(f"{self.url}companies/statements", params=params)

        if response.status_code != 200:
            raise Exception(
                f"Request failed with status code: {response.status_code}, response: {response.text}"
            )

        return response.json()

    def _full_path(self, path):
        if "?" not in path:
            return f"{self.url}{path}?api-key={self.api_key}"
        return f"{self.url}{path}".replace("?", f"?api-key={self.api_key}&")

    def _build_summary_json(self, extracted_data, categories):
        summary_json = {}
        for category, keys in categories.items():
            summary_json[category] = {}
            for key in keys:
                value = extracted_data.get(key)
                if value is None:
                    formatted_value = "N/A"
                elif isinstance(value, (int, float)):
                    formatted_value = f"${value:,}"
                else:
                    formatted_value = value
                summary_json[category][key] = formatted_value
        return summary_json

    def get_derived(self, ticker, fyear, period):
        data = self._get_company_statements(ticker, "derived", fyear, period)
        column_map = {
            "EBITDA": 10,
            "Gross Profit Margin": 13,
            "Operating Margin": 14,
            "Net Profit Margin": 15,
            "Return on Equity": 16,
            "Return on Assets": 17,
            "Return On Invested Capital": 29,
            "Current Ratio": 19,
            "Total Debt": 11,
            "Liabilities to Equity Ratio": 20,
            "Debt Ratio": 21,
            "Free Cash Flow": 12,
            "Free Cash Flow to Net Income": 18,
            "Cash Return On Invested Capital": 30,
            "Earnings Per Share, Basic": 22,
            "Earnings Per Share, Diluted": 23,
            "Sales Per Share": 24,
            "Equity Per Share": 25,
            "Dividends Per Share": 27,
            "Piotroski F-Score": 28,
            "Net Debt / EBITDA": 32,
            "Dividend Payout Ratio": 31,
            "Report Date": 4,
            "Publish Date": 5,
            "Source": 7,
        }
        extracted_data = self._extract_financial_data(data, column_map)
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
            "Per Share Metrics": [
                "Earnings Per Share, Basic",
                "Earnings Per Share, Diluted",
                "Sales Per Share",
                "Equity Per Share",
                "Dividends Per Share",
            ],
            "Other Important Metrics": [
                "Piotroski F-Score",
                "Net Debt / EBITDA",
                "Dividend Payout Ratio",
            ],
            "Metadata": ["Report Date", "Publish Date", "Source"],
        }
        summary_json = self._build_summary_json(extracted_data, column_map)
        return summary_json

    def get_cash_flow(self, ticker, fyear, period):
        data = self._get_company_statements(ticker, "cf", fyear, period)
        column_map = {
            "Net Income": 11,
            "Depreciation & Amortization": 14,
            "Change in Working Capital": 19,
            "Net Cash from Operating Activities": 25,
            "Acquisition of Fixed Assets & Intangibles": 30,
            "Net Cash from Investing Activities": 44,
            "Dividends Paid": 45,
            "Cash from (Repayment of) Debt": 46,
            "Net Cash from Financing Activities": 56,
            "Net Change in Cash": 61,
            "Report Date": 4,
            "Publish Date": 5,
            "Source": 7,
        }

        extracted_data = self._extract_financial_data(data, column_map)
        column_map = {
            "Operating Activities": [
                "Net Income",
                "Depreciation & Amortization",
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
        column_map = {
            "Revenue": 10,
            "Gross Profit": 18,
            "Operating Income (Loss)": 28,
            "Operating Expenses": 20,
            "Interest Expense": 31,
            "Depreciation & Amortization": 25,
            "Earnings Per Share, Basic": 64,
            "Pretax Income (Loss)": 52,
            "Income Tax (Expense) Benefit, Net": 53,
            "Report Date": 4,
            "Publish Date": 5,
            "Source": 7,
        }

        extracted_data = self._extract_financial_data(data, column_map)
        categories = {
            "Income": ["Revenue", "Gross Profit"],
            "Expenses": [
                "Operating Expenses",
                "Interest Expense",
                "Depreciation & Amortization",
            ],
            "Profitability": ["Operating Income (Loss)", "Pretax Income (Loss)"],
            "Taxation": ["Income Tax (Expense) Benefit, Net"],
            "Per Share Metrics": ["Earnings Per Share, Basic"],
            "Metadata": ["Report Date", "Publish Date", "Source"],
        }
        summary_json = self._build_summary_json(extracted_data, categories)
        return summary_json

    def get_balance_sheet(self, ticker, fyear, period):
        data = self._get_company_statements(ticker, "bs", fyear, period)
        column_map = {
            "Cash, Cash Equivalents & Short Term Investments": 10,
            "Accounts & Notes Receivable": 13,
            "Inventories": 17,
            "Other Short Term Assets": 22,
            "Total Current Assets": 30,
            "Total Noncurrent Assets": 49,
            "Total Assets": 50,
            "Accounts Payable": 52,
            "Short Term Debt": 56,
            "Total Current Liabilities": 66,
            "Long Term Debt": 67,
            "Total Noncurrent Liabilities": 81,
            "Total Liabilities": 82,
            "Common Stock": 85,
            "Retained Earnings": 89,
            "Total Equity": 93,
            "Total Liabilities & Equity": 94,
            "Report Date": 4,
            "Publish Date": 5,
            "Source": 7,
        }
        extracted_data = self._extract_financial_data(data, column_map)
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
