# config/settings.py

import os
from dotenv import load_dotenv
from config.constants import *

load_dotenv()

class Settings:
    # Environment
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")

    # Model config
    LLM_MODEL_NAME = "meta-llama/llama-3.3-70b-instruct:free"
    LLM_TEMPERATURE = 0.3
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

    # Paths
    VECTOR_DB_BASE_PATH = VECTOR_DB_BASE_PATH
    UPLOAD_BASE_PATH = UPLOAD_BASE_PATH
    OUTPUT_BASE_PATH = OUTPUT_BASE_PATH
    LOG_BASE_PATH = LOG_BASE_PATH

settings = Settings()
