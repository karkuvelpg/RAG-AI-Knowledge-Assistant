import os
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
MODEL_NAME = "sarvam-m"
TOP_K = 3