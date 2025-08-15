from typing import List
import requests
from langchain_core.embeddings import Embeddings


class NewEmbeddings(Embeddings):
    def __init__(
        self, base_url: str, api_key: str, model: str = "text-embedding-ada-002"
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model

    def _call_embedding_api(self, text: str) -> List[float]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {"model": self.model, "input": text, "encoding_format": "float"}

        response = requests.post(
            f"{self.base_url}/v1/embeddings", json=data, headers=headers
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]

    def embed_query(self, text: str) -> List[float]:
        return self._call_embedding_api(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._call_embedding_api(text) for text in texts]