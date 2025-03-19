import logging
import json
import sys
import os


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)


# Set the log file path to the backend directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE_PATH = os.path.join(BASE_DIR, "app.log")

logger = logging.getLogger(__name__)
formatter = JSONFormatter()
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(LOG_FILE_PATH)
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.handlers = [stream_handler, file_handler]
logger.setLevel(logging.INFO)
