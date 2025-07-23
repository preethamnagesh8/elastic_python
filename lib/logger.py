import logging
import socket
import json
from datetime import datetime, UTC
from elasticsearch import Elasticsearch
from config.config import Config

class ElasticsearchHandler(logging.Handler):
    def __init__(self, hosts, index, username=None, password=None, api_key=None):
        super().__init__()
        self.hostname = socket.gethostname()
        today = datetime.now(UTC).strftime("%Y.%m.%d")
        self.index = f"{index}{today}"

        if api_key:
            self.es = Elasticsearch(
                hosts,
                api_key=api_key
            )
        elif username and password:
            self.es = Elasticsearch(
                hosts,
                basic_auth=(username, password),
                verify_certs=False
            )
        else:
            self.es = Elasticsearch(hosts)

    def emit(self, record):
        log_entry = self.format(record)
        try:
            self.es.index(
                index=self.index,
                body={
                    "@timestamp": datetime.utcnow().isoformat(),
                    "host": self.hostname,
                    **record.__dict__
                }
            )
        except Exception as e:
            print(f"Failed to send log to Elasticsearch: {e}")

def get_logger(name="app_logger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        es_handler = ElasticsearchHandler(
            hosts=[Config.get("ES_HOST")],
            index=Config.get("ES_INDEX"),
            username=Config.get("ES_USERNAME"),
            password=Config.get("ES_PASSWORD")
        )
        es_handler.setFormatter(logging.Formatter('%(message)s'))

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

        logger.addHandler(console_handler)
        logger.addHandler(es_handler)

    return logger