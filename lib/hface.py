import requests
from config.config import Config

class HuggingFaceClient:
    def __init__(self, api_token=None):
        self.api_token = Config.get("HUGGING_FACE_READ_ONLY_TOKEN")
        self.base_url = "https://huggingface.co/api/daily_papers?date=2025-07-22"

    def get_research_papers(self, date):
        url = f"{self.base_url}".format(date=date)
        headers = {}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data

if __name__ == "__main__":
    # Example usage
    client = HuggingFaceClient()
    try:
        papers = client.get_research_papers()
        for paper in papers:
            print(f"Title: {paper.get('title', 'No title')}")
            print(f"Authors: {paper.get('authors', 'No authors')}")
            print(f"Summary: {paper.get('summary', 'No summary')}\n")
    except requests.RequestException as e:
        print(f"Error fetching papers: {e}")