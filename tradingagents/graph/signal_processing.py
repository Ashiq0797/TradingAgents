from tradingagents.llm_provider import SafeLLMWrapper
import random

class SignalProcessor:
    def __init__(self, quick_thinking_llm):
        self.quick_thinking_llm = SafeLLMWrapper(quick_thinking_llm)

    def process_signal(self, full_signal: str) -> str:
        print("\n[DEBUG] Full Signal Input to LLM:\n", full_signal)

        messages = [
            (
                "system",
                "You are a financial assistant. Extract the investment decision: SELL, BUY, or HOLD. "
                "Respond ONLY with one of: SELL, BUY, or HOLD."
            ),
            ("human", full_signal),
        ]
        try:
            response = self.quick_thinking_llm.invoke(messages)
            llm_response = response.content.strip().upper()
            print("[LLM DEBUG RESPONSE]", llm_response)

            # Normalize decision (fuzzy match)
            if "BUY" in llm_response:
                final_decision = "BUY"
            elif "SELL" in llm_response:
                final_decision = "SELL"
            elif "HOLD" in llm_response:
                final_decision = "HOLD"
            else:
                final_decision = "NO DECISION"

            print("[Decision DEBUG]", final_decision)
            return final_decision

        except Exception as e:
            print(f"[ERROR] Hybrid decision failed: {e}")
            return "NO DECISION"
