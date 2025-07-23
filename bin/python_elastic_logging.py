import uuid

from config.config import Config
from lib.logger import get_logger
from core import custom_completions
import schedule
import time

logger = get_logger()

def job():
    logger.info("Job started", extra={"job_id": str(uuid.uuid4())})
    # Basically run this job every x mins
    # Get latest paper from huggingface website
    # Parse the information and try to get the data from it
    # Generate the summary and store it in the database
    logger.info("Job finished")


if __name__ == '__main__':
    x = 1  # Replace with your desired interval in minutes

    schedule.every(x).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)