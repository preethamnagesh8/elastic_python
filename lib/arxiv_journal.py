import arxiv

class ArxivClient:
    def __init__(self):
        self.client = arxiv.Client()

    def get_paper_by_id(self, arxiv_id):
        search = arxiv.Search(id_list=[arxiv_id])
        for result in self.client.results(search):
            return {
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

if __name__ == "__main__":
    # Example usage
    client = ArxivClient()
    arxiv_id = '2507.15846'
    paper = client.get_paper_by_id(arxiv_id)
    if paper:
        pdf_content = client.get_pdf_content(paper['pdf_url'])
        print(f"Downloaded PDF content of length: {len(pdf_content)} bytes")
    else:
        print("Paper not found.")