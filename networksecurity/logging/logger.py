import logging
import os
from datetime import datetime

LOG_FILE= f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}"

log_path=os.path.join(os.getcwd(),'logs',LOG_FILE)
os.makedirs(log_path, exist_ok=True)
LOG_FILE_PATH=os.path.join(log_path,LOG_FILE)

# File handler
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Also log to console so long-running training shows progress in terminal
root_logger = logging.getLogger()
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)
root_logger.addHandler(console_handler)

# Console-only logger for messages that should not go to the file
console_logger = logging.getLogger("console_only")
if not console_logger.handlers:
    _ch = logging.StreamHandler()
    _ch.setLevel(logging.INFO)
    _ch.setFormatter(console_formatter)
    console_logger.addHandler(_ch)
console_logger.propagate = False