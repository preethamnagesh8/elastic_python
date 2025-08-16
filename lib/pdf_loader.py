import asyncio
from langchain_community.document_loaders import PyPDFLoader

def pdf_loader(file_path):
    loader = PyPDFLoader(file_path)
    pages = []
    import re
    pattern = re.compile(r"/uni.{8}")
    for page in loader.lazy_load():
        page.page_content = re.sub(pattern, "", page.page_content)
        pages.append(page)
    return pages

if __name__ == "__main__":
    file_path = "local/pdfs/automated_consistency_analysis_of_llms.pdf"
    data = pdf_loader(file_path)  # Use asyncio.run to call async function
    print(f"Loaded {len(data)} pages")