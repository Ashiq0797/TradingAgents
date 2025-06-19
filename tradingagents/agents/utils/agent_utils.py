from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, AIMessage
from typing import List, Annotated
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import RemoveMessage
from langchain_core.tools import tool
from datetime import date, timedelta, datetime
import functools
import pandas as pd
import os
from dateutil.relativedelta import relativedelta
from tradingagents.llm_provider import get_chat_model
import tradingagents.dataflows.interface as interface
from tradingagents.default_config import DEFAULT_CONFIG
from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage

def create_msg_delete():
    def delete_messages(state):
        """To prevent message history from overflowing, regularly clear message history after a stage of the pipeline is done"""
        messages = state["messages"]
        return {"messages": [RemoveMessage(id=m.id) for m in messages]}
    return delete_messages

def run_streamed_llm_response(prompt: str):
    """Stream a response from the LLM"""
    llm = get_chat_model(model="phi")  # Replace with "mistral" if needed
    stream = llm.stream(prompt)
    print("🔁 Streaming response:\n")
    response_text = ""
    for chunk in stream:
        content = chunk.content if isinstance(chunk, AIMessage) else chunk
        print(content, end="", flush=True)
        response_text += content
    return response_text

class Toolkit:
    _config = DEFAULT_CONFIG.copy()

    @classmethod
    def update_config(cls, config):
        cls._config.update(config)

    @property
    def config(self):
        return self._config

    def __init__(self, config=None):
        if config:
            self.update_config(config)

    @staticmethod
    @tool
    def get_reddit_news(curr_date: Annotated[str, "Date in yyyy-mm-dd"]):
        """Retrieve global news from Reddit."""
        return interface.get_reddit_global_news(curr_date, 7, 5)

    @staticmethod
    @tool
    def get_finnhub_news(ticker: Annotated[str, "Ticker"], start_date: Annotated[str, "Start"], end_date: Annotated[str, "End"]):
        """Retrieve company news from Finnhub."""
        end_date_str = end_date
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        look_back_days = (end_date - start_date).days
        return interface.get_finnhub_news(ticker, end_date_str, look_back_days)

    @staticmethod
    @tool
    def get_reddit_stock_info(ticker: Annotated[str, "Ticker"], curr_date: Annotated[str, "Date"]):
        """Get stock-related Reddit news."""
        return interface.get_reddit_company_news(ticker, curr_date, 7, 5)

    @staticmethod
    @tool
    def get_YFin_data(symbol: Annotated[str, ""], start_date: Annotated[str, ""], end_date: Annotated[str, ""]):
        """Fetch Yahoo Finance historical data."""
        return interface.get_YFin_data(symbol, start_date, end_date)

    @staticmethod
    @tool
    def get_YFin_data_online(symbol: Annotated[str, ""], start_date: Annotated[str, ""], end_date: Annotated[str, ""]):
        """Fetch online Yahoo Finance data."""
        return interface.get_YFin_data_online(symbol, start_date, end_date)

    @staticmethod
    @tool
    def get_stockstats_indicators_report(symbol: Annotated[str, ""], indicator: Annotated[str, ""], curr_date: Annotated[str, ""], look_back_days: Annotated[int, ""] = 30):
        """Get technical indicators report."""
        return interface.get_stock_stats_indicators_window(symbol, indicator, curr_date, look_back_days, False)

    @staticmethod
    @tool
    def get_stockstats_indicators_report_online(symbol: Annotated[str, ""], indicator: Annotated[str, ""], curr_date: Annotated[str, ""], look_back_days: Annotated[int, ""] = 30):
        """Get online technical indicators report."""
        return interface.get_stock_stats_indicators_window(symbol, indicator, curr_date, look_back_days, True)

    @staticmethod
    @tool
    def get_finnhub_company_insider_sentiment(ticker: Annotated[str, ""], curr_date: Annotated[str, ""]):
        """Get company insider sentiment from Finnhub."""
        return interface.get_finnhub_company_insider_sentiment(ticker, curr_date, 30)

    @staticmethod
    @tool
    def get_finnhub_company_insider_transactions(ticker: Annotated[str, ""], curr_date: Annotated[str, ""]):
        """Get insider transactions from Finnhub."""
        return interface.get_finnhub_company_insider_transactions(ticker, curr_date, 30)

    @staticmethod
    @tool
    def get_simfin_balance_sheet(ticker: Annotated[str, ""], freq: Annotated[str, ""], curr_date: Annotated[str, ""]):
        """Get company balance sheet from SimFin."""
        return interface.get_simfin_balance_sheet(ticker, freq, curr_date)

    @staticmethod
    @tool
    def get_simfin_cashflow(ticker: Annotated[str, ""], freq: Annotated[str, ""], curr_date: Annotated[str, ""]):
        """Get cashflow statement from SimFin."""
        return interface.get_simfin_cashflow(ticker, freq, curr_date)

    @staticmethod
    @tool
    def get_simfin_income_stmt(ticker: Annotated[str, ""], freq: Annotated[str, ""], curr_date: Annotated[str, ""]):
        """Get income statement from SimFin."""
        return interface.get_simfin_income_statements(ticker, freq, curr_date)

    @staticmethod
    @tool
    def get_google_news(query: Annotated[str, ""], curr_date: Annotated[str, ""]):
        """Get latest Google News headlines."""
        return interface.get_google_news(query, curr_date, 7)

    @staticmethod
    @tool
    def get_stock_news_openai(ticker: Annotated[str, ""], curr_date: Annotated[str, ""]):
        """Get stock news using OpenAI."""
        return interface.get_stock_news_openai(ticker, curr_date)

    @staticmethod
    @tool
    def get_global_news_openai(curr_date: Annotated[str, ""]):
        """Get macroeconomic news using OpenAI."""
        return interface.get_global_news_openai(curr_date)

    @staticmethod
    @tool
    def get_fundamentals_openai(ticker: Annotated[str, ""], curr_date: Annotated[str, ""]):
        """Get stock fundamentals using OpenAI."""
        return interface.get_fundamentals_openai(ticker, curr_date)

    @staticmethod
    @tool
    def ask_llm_streamed(prompt: Annotated[str, "Ask the model any trading-related question"]) -> str:
        """Stream a direct question to the LLM."""
        return run_streamed_llm_response(prompt)
