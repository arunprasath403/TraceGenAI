# config/logging_config.py

import logging
import os
from config.constants import LOG_BASE_PATH

def setup_logger(project_id: str) -> logging.Logger:
    os.makedirs(LOG_BASE_PATH, exist_ok=True)

    logger = logging.getLogger(project_id)
    logger.setLevel(logging.INFO)

    log_file = os.path.join(LOG_BASE_PATH, f"{project_id}.log")

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
