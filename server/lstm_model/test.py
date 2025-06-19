import os

MODEL_DIR = "server/lstm_model/models"
MODEL_FILE = "NVDA_lstm.keras"

model_path = os.path.join(MODEL_DIR, MODEL_FILE)

print(f"Checking path: {model_path}")
print("Absolute path:", os.path.abspath(model_path))
print("File exists:", os.path.isfile(model_path))
