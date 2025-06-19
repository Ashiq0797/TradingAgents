import os
import concurrent.futures
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Flags from environment or defaults
USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"
TIMEOUT_SECONDS = int(os.getenv("LLM_TIMEOUT", 15))  # Max wait for LLM

# List of mock decisions to rotate for dev/test
MOCK_DECISIONS = ["BUY", "SELL", "HOLD"]

def get_chat_model(model="mistral", **kwargs):
    model = model or os.getenv("OLLAMA_MODEL", "mistral")  # 🔧 Fetch from .env or fallback
    if MOCK_MODE:
        return MockLLM()

    if USE_OLLAMA:
        try:
            return ChatOllama(
                model=model,
                temperature=0,
                streaming=False,
                options={
                    "num_predict": 1,
                    "num_gpu_layers": 100,
                    "top_k": 20,
                    "top_p": 0.9,
                    "stop": ["\n"]
                }
            )
        except Exception as e:
            print(f"[LLM WARNING] Ollama failed: {e}. Falling back to OpenAI.")
    
    # Fallback: OpenAI GPT
    return ChatOpenAI(model="gpt-3.5-turbo", **kwargs)


class SafeLLMWrapper:
    def __init__(self, llm):
        self.llm = llm

    def invoke(self, messages):
        """Run LLM with a timeout."""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.llm.invoke, messages)
            try:
                return future.result(timeout=TIMEOUT_SECONDS)
            except concurrent.futures.TimeoutError:
                print(f"[LLM TIMEOUT] LLM response exceeded {TIMEOUT_SECONDS} seconds.")
                return type("FakeResponse", (), {"content": "HOLD"})()  # Safe fallback


class MockLLM:
    def __init__(self):
        import random
        self.choices = MOCK_DECISIONS
        self.index = 0

    def invoke(self, messages):
        decision = self.choices[self.index % len(self.choices)]
        self.index += 1
        print(f"[MOCK LLM RESPONSE] {decision}")
        return type("FakeResponse", (), {"content": decision})()
