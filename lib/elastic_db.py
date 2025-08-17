from typing import Optional

from config.config import Config
from elasticsearch import Elasticsearch

class ElasticDB:
    def __init__(
        self,
        es_username: str,
        es_password: str,
        index_name: str,
    ):
        self.index_name = index_name
        self.es_client = Elasticsearch(
            [Config.get("ES_HOST")],
            basic_auth=(es_username, es_password),
            verify_certs=False
        )

    def store(self, doc_id: str, data: dict):
        """
        Store a document in Elasticsearch under the given index.
        """
        self.es_client.index(index=self.index_name, id=doc_id, document=data)

    def retrieve(self, doc_id: str) -> Optional[dict]:
        """
        Retrieve a document from Elasticsearch by ID.
        """
        try:
            result = self.es_client.get(index=self.index_name, id=doc_id)
            return result["_source"]
        except Exception:
            return None

    def update(self, doc_id: str, data: dict):
        """
        Update a document in Elasticsearch under the given index.
        """
        self.es_client.update(index=self.index_name, id=doc_id, doc=data)

    def exists(self, doc_id: str) -> bool:
        """
        Check if a document exists in Elasticsearch by ID.
        """
        try:
            return self.es_client.exists(index=self.index_name, id=doc_id)
        except Exception:
            return False