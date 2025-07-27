import arxiv
import pdfplumber
import io
import requests
from langchain.document_loaders import PyPDFLoader
import re
import unicodedata


class ArxivClient:
    def __init__(self):
        self.client = arxiv.Client()

    def get_paper_by_id(self, arxiv_id):
        search = arxiv.Search(id_list=[arxiv_id])
        for result in self.client.results(search):
            return {
                "id": f"arxiv_{arxiv_id}",
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary,
                "published": result.published,
                "pdf_url": result.pdf_url
            }
        return None

    def get_pdf_content(self, pdf_url):
        import requests
        response = requests.get(pdf_url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to download PDF: {response.status_code}")

    def download_file(id, url, local_path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path + f"{id}.pdf", "wb") as f:
                f.write(response.content)
        else:
            raise Exception(f"Failed to download file: {response.status_code}")

    def extract_text_from_pdf(pdf_bytes):
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text


    def clean_text(text: str) -> str:
        # Normalize Unicode characters
        text = unicodedata.normalize('NFKD', text)
        # Remove non-printable characters
        text = ''.join(ch for ch in text if ch.isprintable())
        # Remove unwanted special chars except common punctuation
        text = re.sub(r'[^\w\s.,;:?!\'\"-]', '', text)
        # Replace multiple spaces and newlines with a single space
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

if __name__ == "__main__":
    # Example usage
    client = ArxivClient()
    arxiv_id = '2507.15846'
    paper = client.get_paper_by_id(arxiv_id)
    if paper:
        download_path = "/Users/preethamnagesh8/MyProjects/python_elastic_logging/elastic_python/local/docs/"
        ArxivClient.download_file(paper['id'], paper['pdf_url'], download_path)
        loader = PyPDFLoader(download_path + f"{paper['id']}.pdf")
        documents = loader.load()

        # Extract text content and clean
        all_text = []
        for doc in documents:
            cleaned = ArxivClient.clean_text(doc.page_content)
            all_text.append(cleaned)

        a = 10
    else:
        print("Paper not found.")