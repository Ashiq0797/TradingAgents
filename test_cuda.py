import torch

# Check PyTorch version
print("PyTorch version:", torch.__version__)

# Check if CUDA is available
print("CUDA available:", torch.cuda.is_available())

# Check GPU name if available
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
