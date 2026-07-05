"""
Настройка логгирования
"""


import os
from logging import getLogger, basicConfig, INFO, DEBUG, WARNING, ERROR, CRITICAL, StreamHandler, FileHandler
from dotenv import load_dotenv

# Load environment variables from .env.config located at project root
load_dotenv()

def setup_logging():
    # Determine log level from LOG_LEVEL env var, fallback to INFO
    level_name = os.getenv('LOG_LEVEL', 'INFO').upper()
    level = {
        'DEBUG': DEBUG,
        'INFO': INFO,
        'WARNING': WARNING,
        'ERROR': ERROR,
        'CRITICAL': CRITICAL,
    }.get(level_name, INFO)

    # Ensure logs directory exists
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, 'app.log')

    # Configure root logger: console + file handlers
    log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    basicConfig(
        level=level,
        format=log_format,
        handlers=[
            # File handler
            FileHandler(log_file, encoding='utf-8'),
            # Console handler
            StreamHandler()
        ]
    )

