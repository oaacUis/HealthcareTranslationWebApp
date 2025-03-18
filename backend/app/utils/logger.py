import logging
import json
import sys


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)


logger = logging.getLogger(__name__)
formatter = JSONFormatter()
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("app.log")
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.handlers = [stream_handler, file_handler]
logger.setLevel(logging.INFO)
