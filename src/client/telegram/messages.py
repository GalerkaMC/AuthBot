import os
from dotenv import load_dotenv

load_dotenv()

MESSAGES = {
    "start": os.getenv("MSG_START", "PLACEHOLDER start message"),
    "help": os.getenv("MSG_HELP", "PLACEHOLDER help message"),
    "auth_prompt": os.getenv("MSG_AUTH_PROMPT", "PLACEHOLDER auth prompt"),
    "result_successful": os.getenv("MSG_RESULT_SUCCESS", "PLACEHOLDER success message"),
    "result_expired": os.getenv("MSG_RESULT_EXPIRED", "PLACEHOLDER expired message"),
    "result_illegal": os.getenv("MSG_RESULT_ILLEGAL", "PLACEHOLDER illegal message"),
}
