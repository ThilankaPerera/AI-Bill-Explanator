import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploaded_bills"

# Create directories if they don't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# LLM Configuration
LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"  # Open source model
LLM_TEMPERATURE = 0.3
MAX_TOKENS = 2000

