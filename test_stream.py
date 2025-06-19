from tradingagents.llm_provider import get_chat_model

# Use smaller model for faster response (you can switch to "mistral-gpu" later)
llm = get_chat_model(model="phi")

print("Streaming response:\n")
response_stream = llm.stream("What is the fastest land animal?")

for chunk in response_stream:
    print(chunk.content, end="", flush=True)
