import os
from dotenv import load_dotenv

load_dotenv()

# Model Settings
PRIMARY_MODEL = os.getenv("PRIMARY_MODEL", "gemini-2.0-flash")
CHEAP_MODEL = os.getenv("CHEAP_MODEL", "gemini-2.0-flash-lite")

# Cost Estimation (Placeholder values)
COST_PER_1K_TOKENS = {
    "gemini-2.0-flash": 0.0001,
    "gemini-2.0-flash-lite": 0.00005
}

# Project Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_DIR = os.path.join(BASE_DIR, "data/memory")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Ensure directories exist
os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
