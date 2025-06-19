import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEFAULT_CONFIG = {
    "project_dir": BASE_DIR,
    "data_dir": os.path.join(BASE_DIR, "dataflows"),  # adjust if you have another path
    "data_cache_dir": os.path.join(BASE_DIR, "dataflows", "data_cache"),

    # LLM settings
    "deep_think_llm": "mistral",
    "quick_think_llm": "mistral",

    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,

    # Tool settings
    "online_tools": False  # ← set to False unless you’re enabling web scraping/tools
}
