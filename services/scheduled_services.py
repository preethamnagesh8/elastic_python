import schedule
import time
from bin.python_elastic_logging import job

def run_job():
    job()

schedule.every(2).hours.do(run_job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)