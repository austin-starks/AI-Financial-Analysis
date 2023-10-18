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

    def _full_path(self, path):
        if "?" not in path:
            return f"{self.url}{path}?api-key={self.api_key}"
        return f"{self.url}{path}".replace("?", f"?api-key={self.api_key}&")

    def _get_derived(self, ticker, fyear, period):
        response = requests.get(
            self._full_path(f"companies/statements"),
            params={
                "ticker": ticker,
                "statement": "derived",
                "fyear": fyear,
                "period": period,
            },
        )
        if response.status_code != 200:
            raise Exception(
                f"Request failed with status code: {response.status_code}, response: {response.text}"
            )
        data = response.json()
        column_map = {
            # Profitability Metrics
            "EBITDA": 10,
            "Gross Profit Margin": 13,
            "Operating Margin": 14,
            "Net Profit Margin": 15,
            "Return on Equity": 16,
            "Return on Assets": 17,
            "Return On Invested Capital": 29,
            # Liquidity Metrics
            "Current Ratio": 19,
            # Solvency Metrics
            "Total Debt": 11,
            "Liabilities to Equity Ratio": 20,
            "Debt Ratio": 21,
            # Cash Flow Metrics
            "Free Cash Flow": 12,
            "Free Cash Flow to Net Income": 18,
            "Cash Return On Invested Capital": 30,
            # Per Share Metrics
            "Earnings Per Share, Basic": 22,
            "Earnings Per Share, Diluted": 23,
            "Sales Per Share": 24,
            "Equity Per Share": 25,
            "Dividends Per Share": 27,
            # Other Important Metrics
            "Piotroski F-Score": 28,
            "Net Debt / EBITDA": 32,
            "Dividend Payout Ratio": 31,
            "Report Date": 4,
            "Publish Date": 5,
            "Source": 7,
        }
        extracted_data = self._extract_financial_data(data, column_map)
        summary_json = {
            "Profitability Metrics": {},
            "Liquidity Metrics": {},
            "Solvency Metrics": {},
            "Cash Flow Metrics": {},
            "Per Share Metrics": {},
            "Other Important Metrics": {},
            "Metadata": {},
        }

        # Profitability Metrics
        for key in [
            "EBITDA",
            "Gross Profit Margin",
            "Operating Margin",
            "Net Profit Margin",
            "Return on Equity",
            "Return on Assets",
            "Return On Invested Capital",
        ]:
            value = extracted_data.get(key)
            summary_json["Profitability Metrics"][key] = (
                f"{value}" if value is not None else "N/A"
            )

        # Liquidity Metrics
        for key in ["Current Ratio"]:
            value = extracted_data.get(key)
            summary_json["Liquidity Metrics"][key] = (
                f"{value}" if value is not None else "N/A"
            )

        # Solvency Metrics
        for key in ["Total Debt", "Liabilities to Equity Ratio", "Debt Ratio"]:
            value = extracted_data.get(key)
            summary_json["Solvency Metrics"][key] = (
                f"{value}" if value is not None else "N/A"
            )

        # Cash Flow Metrics
        for key in [
            "Free Cash Flow",
            "Free Cash Flow to Net Income",
            "Cash Return On Invested Capital",
        ]:
            value = extracted_data.get(key)
            summary_json["Cash Flow Metrics"][key] = (
                f"{value}" if value is not None else "N/A"
            )

        # Per Share Metrics
        for key in [
            "Earnings Per Share, Basic",
            "Earnings Per Share, Diluted",
            "Sales Per Share",
            "Equity Per Share",
            "Dividends Per Share",
        ]:
            value = extracted_data.get(key)
            summary_json["Per Share Metrics"][key] = (
                f"{value}" if value is not None else "N/A"
            )

        # Other Important Metrics
        for key in ["Piotroski F-Score", "Net Debt / EBITDA", "Dividend Payout Ratio"]:
            value = extracted_data.get(key)
            summary_json["Other Important Metrics"][key] = (
                f"{value}" if value is not None else "N/A"
            )

        # Metadata
        for key in ["Report Date", "Publish Date", "Source"]:
            value = extracted_data.get(key)
            summary_json["Metadata"][key] = value if value is not None else "N/A"

        return summary_json

    def _get_cash_flow(self, ticker, fyear, period):
        response = requests.get(
            self._full_path(f"companies/statements"),
            params={
                "ticker": ticker,
                "statement": "cf",
                "fyear": fyear,
                "period": period,
            },
        )
        if response.status_code != 200:
            raise Exception(
                f"Request failed with status code: {response.status_code}, response: {response.text}"
            )
        data = response.json()

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

        summary_json = {
            "Operating Activities": {},
            "Investing Activities": {},
            "Financing Activities": {},
            "Net Change": {},
            "Metadata": {},
        }

        # Operating Activities
        for key in [
            "Net Income",
            "Depreciation & Amortization",
            "Change in Working Capital",
            "Net Cash from Operating Activities",
        ]:
            value = extracted_data.get(key)
            summary_json["Operating Activities"][key] = (
                f"${value:,}" if value is not None else "N/A"
            )

        # Investing Activities
        for key in [
            "Acquisition of Fixed Assets & Intangibles",
            "Net Cash from Investing Activities",
        ]:
            value = extracted_data.get(key)
            summary_json["Investing Activities"][key] = (
                f"${value:,}" if value is not None else "N/A"
            )

        # Financing Activities
        for key in [
            "Dividends Paid",
            "Cash from (Repayment of) Debt",
            "Net Cash from Financing Activities",
        ]:
            value = extracted_data.get(key)
            summary_json["Financing Activities"][key] = (
                f"${value:,}" if value is not None else "N/A"
            )

        # Net Change
        for key in ["Net Change in Cash"]:
            value = extracted_data.get(key)
            summary_json["Net Change"][key] = (
                f"${value:,}" if value is not None else "N/A"
            )

        # Metadata
        for key in ["Report Date", "Publish Date", "Source"]:
            value = extracted_data.get(key)
            summary_json["Metadata"][key] = value if value is not None else "N/A"

        return summary_json

    def _get_profit_loss(self, ticker, fyear, period):
        response = requests.get(
            self._full_path(f"companies/statements"),
            params={
                "ticker": ticker,
                "statement": "pl",
                "fyear": fyear,
                "period": period,
            },
        )
        if response.status_code != 200:
            raise Exception(
                f"Request failed with status code: {response.status_code}, response: {response.text}"
            )
        data = response.json()

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
        summary_json = {
            "Income": {},
            "Expenses": {},
            "Profitability": {},
            "Taxation": {},
            "Per Share Metrics": {},
            "Metadata": {},
        }
        # Income
        for key in ["Revenue", "Gross Profit"]:
            value = extracted_data.get(key)
            summary_json["Income"][key] = f"${value:,}" if value is not None else "N/A"

        # Expenses
        for key in [
            "Operating Expenses",
            "Interest Expense",
            "Depreciation & Amortization",
        ]:
            value = extracted_data.get(key)
            summary_json["Expenses"][key] = (
                f"${value:,}" if value is not None else "N/A"
            )

        # Profitability
        for key in ["Operating Income (Loss)", "Pretax Income (Loss)"]:
            value = extracted_data.get(key)
            summary_json["Profitability"][key] = (
                f"${value:,}" if value is not None else "N/A"
            )

        # Taxation
        for key in ["Income Tax (Expense) Benefit, Net"]:
            value = extracted_data.get(key)
            summary_json["Taxation"][key] = (
                f"${value:,}" if value is not None else "N/A"
            )

        # Per Share Metrics
        for key in ["Earnings Per Share, Basic"]:
            value = extracted_data.get(key)
            summary_json["Per Share Metrics"][key] = (
                f"${value:,}" if value is not None else "N/A"
            )

        # Metadata
        for key in ["Report Date", "Publish Date", "Source"]:
            value = extracted_data.get(key)
            summary_json["Metadata"][key] = value if value is not None else "N/A"
        return summary_json

    def _get_balance_sheet(self, ticker, fyear, period):
        response = requests.get(
            self._full_path(f"companies/statements"),
            params={
                "ticker": ticker,
                "statement": "bs",
                "fyear": fyear,
                "period": period,
            },
        )
        if response.status_code != 200:
            raise Exception(
                f"Request failed with status code: {response.status_code}, response: {response.text}"
            )
        data = response.json()
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
        summary_json = {
            "Assets": {},
            "Liabilities": {},
            "Equity": {},
            "Summary": {},
            "Metadata": {},
        }

        for key in [
            "Cash, Cash Equivalents & Short Term Investments",
            "Accounts & Notes Receivable",
            "Inventories",
            "Other Short Term Assets",
            "Total Current Assets",
            "Total Noncurrent Assets",
            "Total Assets",
        ]:
            value = extracted_data.get(key)
            summary_json["Assets"][key] = f"${value:,}" if value is not None else "N/A"

        for key in [
            "Accounts Payable",
            "Short Term Debt",
            "Total Current Liabilities",
            "Long Term Debt",
            "Total Noncurrent Liabilities",
            "Total Liabilities",
        ]:
            value = extracted_data.get(key)
            summary_json["Liabilities"][key] = (
                f"${extracted_data[key]:,}" if value is not None else "N/A"
            )

        for key in ["Common Stock", "Retained Earnings", "Total Equity"]:
            value = extracted_data.get(key)
            summary_json["Equity"][key] = (
                f"${extracted_data[key]:,}" if value is not None else "N/A"
            )

        for key in ["Report Date", "Publish Date", "Source"]:
            value = extracted_data.get(key)
            summary_json["Metadata"][key] = value if value is not None else "N/A"

        value = extracted_data.get("Total Liabilities & Equity")
        summary_json["Summary"]["Total Liabilities & Equity"] = (
            f"${value:,} - This should equal the Total Assets, as per the accounting equation Assets = Liabilities + Equity."
            if value is not None
            else "N/A"
        )
        return summary_json

    def get_financials(self, ticker, fyear, period):
        balance_json = self._get_balance_sheet(ticker, fyear, period)
        cash_flow_json = self._get_cash_flow(ticker, fyear, period)
        derived_json = self._get_derived(ticker, fyear, period)
        profit_loss_json = self._get_profit_loss(ticker, fyear, period)
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
