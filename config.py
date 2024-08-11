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

# Sri Lankan specific configurations
CURRENCY = "LKR"
COMMON_UTILITIES = ["CEB", "Ceylon Electricity Board", "LECO", 
                    "National Water Supply", "Dialog", "Mobitel", 
                    "Hutch", "Airtel", "SLT"]

# Common bill types in Sri Lanka
BILL_TYPES = {
    "electricity": ["CEB", "LECO", "electricity", "power"],
    "water": ["water", "National Water Supply", "NWSDB"],
    "telecom": ["Dialog", "Mobitel", "Hutch", "Airtel", "SLT", "mobile", "internet"],
    "hospital": ["hospital", "medical", "clinic", "healthcare"]
}

# Common charges and taxes in Sri Lanka
SL_TAXES = {
    "VAT": 15,  # Value Added Tax
    "NBT": 2,   # Nation Building Tax
    "Levy": None  # Various levies
}

# Anomaly detection thresholds
ANOMALY_THRESHOLD = 1.5  # 50% increase from average