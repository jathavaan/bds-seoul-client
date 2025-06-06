from datetime import datetime
import logging
import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()


class Config(Enum):
    KAFKA_BOOTSTRAP_SERVERS = f"{os.getenv('KAFKA_BOOTSTRAP_SERVERS')}:9092"
    KAFKA_GROUP_ID = "seoul"

    KAFKA_REVIEW_TOPIC = "reviews"
    KAFKA_FINAL_RESULT_TOPIC = "final_results"
    KAFKA_LAST_SCRAPED_DATE_REQ_TOPIC = "last_scraped_date_requests"
    KAFKA_LAST_SCRAPED_DATE_RES_TOPIC = "last_scraped_date_responses"
    KAFKA_PROCESS_STATUS_TOPIC = "process_status"

    KAFKA_POLL_TIMEOUT = 1.0

    KAFKA_SESSION_TIMEOUT = 120000
    KAFKA_MAX_POLL_TIMEOUT = 86400000
    KAFKA_HEARTBEAT_INTERVAL = 3000

    LOGGING_LEVEL = logging.INFO
    LOGGER_WIDTH_OFFSET = 90
    SEQ_URL = f"http://{os.getenv('SEQ_SERVER')}:{os.getenv('SEQ_PORT')}"
    SEQ_LOG_BATCH_SIZE = 1

    CUTOFF_DATE = datetime.strptime(f'2014-05-26', "%Y-%m-%d")  # TODO: Remove this. Cutoff date is dynamic
    TARGET_REVIEW_COUNT = 10000

    BROWSER_PATH = "/usr/bin/firefox-esr"
    DRIVER_PATH = "/usr/local/bin/geckodriver"
    GECKODRIVER_HOST = "http://localhost:4444"
