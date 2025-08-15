import uuid
from langchain_core.messages import SystemMessage, HumanMessage
from config.config import Config
from lib.logger import get_logger
from core import custom_completions
import schedule
import time
from lib.arxiv_journal import ArxivClient
from lib.hface import HuggingFaceClient
from datetime import date
from langchain.document_loaders import PyPDFLoader
from core.custom_completions import NewGPT
from core.custom_embeddings import NewEmbeddings
from lib.elastic_rag import ElasticRAG
import os
from lib.pdf_loader import pdf_loader
from lib.rag_chunking import chunk_documents

logger = get_logger()

def job():
    logger.info("Job started", extra={"job_id": str(uuid.uuid4())})
    arxiv_client = ArxivClient()
    hface_client = HuggingFaceClient()
    embedding_model = NewEmbeddings(
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_RAG_API_SECRET"),
        model=os.getenv("EMBEDDING_MODEL"),
    )
    llm = NewGPT(
        base_url=os.getenv("OPENAI_BASE_URL"),
        api_key=os.getenv("OPENAI_RAG_API_SECRET"),
        model=os.getenv("OPENAI_CHAT_MODEL"),
    )
    elastic_rag = ElasticRAG(Config.get("ES_USERNAME"), Config.get("ES_PASSWORD"),embedding_model, llm)
    try:
        today_date_str = date.today().strftime("%Y-%m-%d")

        research_papers = hface_client.get_research_papers(today_date_str)
        for res_paper in research_papers:
            logger.info(f"Paper found: {res_paper.get('title', 'No title')}", extra={"job_id": str(uuid.uuid4())})
            paper = arxiv_client.get_paper_by_id(res_paper['paper']['id'])
            arxiv_client.download_file(paper['id'], paper['pdf_url'], Config.get("DOWNLOAD_PATH", "local/docs/"))

            pages = pdf_loader(Config.get("DOWNLOAD_PATH", "local/docs/") + f"{paper['id']}.pdf")
            chunks = chunk_documents(pages)

            chunk_texts = []
            questions = []
            for chunk in chunks:
                question = llm.invoke(
                    [
                        SystemMessage(
                            content=(
                                "You are a helpful assistant. Based on the context provided, "
                                "generate a clear, insightful, and easy-to-understand question "
                                "that relates closely to the key information in the text. "
                                "Provide the question in plain text only—no styling, formatting, or markdown."
                            )
                        ),
                        HumanMessage(
                            content=f"Context:\n{chunk}\n\nPlease generate a relevant question based on the above context."),
                    ]
                )
                questions.append(question.content)
                chunk_texts.append(chunk.page_content)


            unique_questions = llm.invoke(
                [
                    SystemMessage(
                        content=(
                            "You are a helpful assistant. Based on the list of questions provided, "
                            "generate 5 short and simple questions that together form a logical flow, starting with an introduction, "
                            "then moving to more detailed aspects, and finally concluding, as if explaining the topic in an article. "
                            "Ensure each question is clear, insightful, and in plain text only—no styling, formatting, or markdown. "
                            "Return the questions as a comma separated list of strings."
                        )
                    ),
                    HumanMessage(
                        content=f"Questions:\n{questions}\n\nPlease generate 5 logically ordered questions (introduction, details, conclusion) based on the above questions."
                    ),
                ]
            )

            elastic_rag.ingest_documents(chunk_texts)

            ques = unique_questions.content.split(",")

            for q in ques:
                answer = elastic_rag.query(q)
                logger.info(f"Question: {q} | Answer: {answer}", extra={"job_id": str(uuid.uuid4())})

    except Exception as e:
        logger.error(f"Error fetching paper: {e}", extra={"job_id": str(uuid.uuid4())})
    logger.info("Job finished")


if __name__ == '__main__':
    x = 1  # Replace with your desired interval in minutes
    job()

    # schedule.every(x).minutes.do(job)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)