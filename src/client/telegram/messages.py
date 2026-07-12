import os
from dotenv import load_dotenv

load_dotenv(".env.config")

MESSAGES = {
    "start": os.getenv("MSG_START", "PLACEHOLDER start message").replace("\\n", "\n"),
    "apply_name": os.getenv("APPLY_PROMPT_NAME", "Enter name:").replace("\\n", "\n"),
    "apply_nick": os.getenv("APPLY_PROMPT_NICK", "Enter Minecraft nick:").replace("\\n", "\n"),
    "apply_source": os.getenv("APPLY_PROMPT_SOURCE", "Where did you hear about server?").replace("\\n", "\n"),
    "apply_success_user": os.getenv("APPLY_SUCCESS_USER", "Application accepted!").replace("\\n", "\n"),
    "apply_reject_user": os.getenv("APPLY_REJECT_USER", "Application rejected.").replace("\\n", "\n"),
    "apply_blocked_user": os.getenv("APPLY_BLOCKED_USER", "You are blocked from applying.").replace("\\n", "\n"),
    "apply_btn_accept": os.getenv("APPLY_ADMIN_BUTTON_ACCEPT", "Accept").replace("\\n", "\n"),
    "apply_btn_reject": os.getenv("APPLY_ADMIN_BUTTON_REJECT", "Reject").replace("\\n", "\n"),
    "apply_btn_block": os.getenv("APPLY_ADMIN_BUTTON_BLOCK", "Block").replace("\\n", "\n"),
    "apply_already_in_whitelist": os.getenv("APPLY_ALREADY_IN_WHITELIST", "Already exists.").replace("\\n", "\n"),
    "help": os.getenv("MSG_HELP", "PLACEHOLDER help message").replace("\\n", "\n"),
    "auth_prompt": os.getenv("MSG_AUTH_PROMPT", "PLACEHOLDER auth prompt").replace("\\n", "\n"),
    "result_successful": os.getenv("MSG_RESULT_SUCCESS", "PLACEHOLDER success message").replace("\\n", "\n"),
    "result_expired": os.getenv("MSG_RESULT_EXPIRED", "PLACEHOLDER expired message").replace("\\n", "\n"),
    "result_illegal": os.getenv("MSG_RESULT_ILLEGAL", "PLACEHOLDER illegal message").replace("\\n", "\n"),
    "confirm_auth_button_test": os.getenv("CONFIRM_AUTH_BUTTON_TEXT", "Confirm").replace("\\n", "\n"),
    "apply_forbidden": os.getenv("APPLY_FORBIDDEN").replace("\\n", "\n"),
    "apply_request_status_apply": os.getenv("APPLY_REQUEST_STATUS_APPLY").replace("\\n", "\n"),
    "apply_request_status_reject": os.getenv("APPLY_REQUEST_STATUS_REJECT").replace("\\n", "\n"),
    "apply_request_status_blocked": os.getenv("APPLY_REQUEST_STATUS_BLOCKED").replace("\\n", "\n"),
    "apply_send_to_admins": os.getenv("APPLY_SEND_TO_ADMINS").replace("\\n", "\n"),
    "apply_nickname_already_exists": os.getenv("APPLY_NICKNAME_ALREADY_EXISTS").replace("\\n", "\n"),
    "apply_nickname_is_invalid": os.getenv("APPLY_NICKNAME_IS_INVALID").replace("\\n", "\n"),
    "apply_form_input_canceled": os.getenv("APPLY_FORM_INPUT_CANCELED").replace("\\n", "\n")
}
