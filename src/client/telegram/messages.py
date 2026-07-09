import os
from dotenv import load_dotenv

load_dotenv(".env.config")

MESSAGES = {
    "start": os.getenv("MSG_START", "PLACEHOLDER start message"),
    "apply_name": os.getenv("APPLY_PROMPT_NAME", "Enter name:"),
    "apply_nick": os.getenv("APPLY_PROMPT_NICK", "Enter Minecraft nick:"),
    "apply_source": os.getenv("APPLY_PROMPT_SOURCE", "Where did you hear about server?"),
    "apply_success_user": os.getenv("APPLY_SUCCESS_USER", "Application accepted!"),
    "apply_reject_user": os.getenv("APPLY_REJECT_USER", "Application rejected."),
    "apply_blocked_user": os.getenv("APPLY_BLOCKED_USER", "You are blocked from applying."),
    "apply_btn_accept": os.getenv("APPLY_ADMIN_BUTTON_ACCEPT", "Accept"),
    "apply_btn_reject": os.getenv("APPLY_ADMIN_BUTTON_REJECT", "Reject"),
    "apply_btn_block": os.getenv("APPLY_ADMIN_BUTTON_BLOCK", "Block"),
    "apply_already_in_whitelist": os.getenv("APPLY_ALREADY_IN_WHITELIST", "Already exists."),
    "help": os.getenv("MSG_HELP", "PLACEHOLDER help message"),
    "auth_prompt": os.getenv("MSG_AUTH_PROMPT", "PLACEHOLDER auth prompt"),
    "result_successful": os.getenv("MSG_RESULT_SUCCESS", "PLACEHOLDER success message"),
    "result_expired": os.getenv("MSG_RESULT_EXPIRED", "PLACEHOLDER expired message"),
    "result_illegal": os.getenv("MSG_RESULT_ILLEGAL", "PLACEHOLDER illegal message"),
    "confirm_auth_button_test": os.getenv("CONFIRM_AUTH_BUTTON_TEXT", "Confirm"),
    "apply_forbidden": os.getenv("APPLY_FORBIDDEN"),
    "apply_request_status_apply": os.getenv("APPLY_REQUEST_STATUS_APPLY"),
    "apply_request_status_reject": os.getenv("APPLY_REQUEST_STATUS_REJECT"),
    "apply_request_status_blocked": os.getenv("APPLY_REQUEST_STATUS_BLOCKED"),
    "apply_send_to_admins": os.getenv("APPLY_SEND_TO_ADMINS"),
    "apply_nickname_already_exists": os.getenv("APPLY_NICKNAME_ALREADY_EXISTS"),
    "apply_nickname_is_invalid": os.getenv("APPLY_NICKNAME_IS_INVALID"),
    "apply_form_input_canceled": os.getenv("APPLY_FORM_INPUT_CANCELED")
}
