from services.core.scheduler.base import ScheduledJob
import uuid
from langchain_core.messages import SystemMessage, HumanMessage
from config.config import Config
from lib.logger import get_logger
from lib.arxiv_journal import ArxivClient
from lib.hface import HuggingFaceClient
from datetime import date
from core.custom_completions import NewGPT
from core.custom_embeddings import NewEmbeddings
from lib.elastic_rag import ElasticRAG
import os
from lib.pdf_loader import pdf_loader
from lib.rag_chunking import chunk_documents
from lib.elastic_db import ElasticDB
from models.status import PaperStatus

logger = get_logger()

class HFaceResearchIngestionService(ScheduledJob):
    """
    Scheduled job for ingesting research documents into the HFace system.
    This job handles the ingestion of research documents, including PDF loading,
    chunking, embedding, and storing in a vector store.
    """

    def __init__(self):
        self.arxiv_client = ArxivClient()
        self.hface_client = HuggingFaceClient()
        self.embedding_model = NewEmbeddings(
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("OPENAI_RAG_API_SECRET"),
            model=os.getenv("EMBEDDING_MODEL"),
        )
        self.llm = NewGPT(
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("OPENAI_RAG_API_SECRET"),
            model=os.getenv("OPENAI_CHAT_MODEL"),
        )
        self.elastic_rag = ElasticRAG(Config.get("ES_USERNAME"), Config.get("ES_PASSWORD"), self.embedding_model, self.llm)
        self.aegis_questions_index = ElasticDB(Config.get("ES_USERNAME"), Config.get("ES_PASSWORD"), Config.get("AEGIS_QUESTIONS_INDEX"))

    def check_whether_paper_is_ingested(self, paper_id: str) -> bool:
        """
        Check if a paper is already ingested by looking it up in the Aegis questions index.
        :param paper_id: The ID of the paper to check.
        :return: True if the paper is ingested, False otherwise.
        """
        return self.aegis_questions_index.exists(paper_id)

    def run_automtion(self, **kwargs):
        today_date_str = date.today().strftime("%Y-%m-%d")
        research_papers = self.hface_client.get_research_papers(today_date_str)

        for res_paper in research_papers:
            logger.info(f"Paper found: {res_paper.get('title', 'No title')}", extra={"job_id": str(uuid.uuid4())})
            paper = self.arxiv_client.get_paper_by_id(res_paper['paper']['id'])

            if self.check_whether_paper_is_ingested(paper['id']):
                logger.info(f"Paper {paper['id']} is already ingested, skipping.", extra={"job_id": str(uuid.uuid4())})
                continue

            self.arxiv_client.download_file(paper['id'], paper['pdf_url'], Config.get("DOWNLOAD_PATH", "local/docs/"))

            pages = pdf_loader(Config.get("DOWNLOAD_PATH", "local/docs/") + f"{paper['id']}.pdf")
            chunks = chunk_documents(pages)

            chunk_texts = []
            questions = []
            for chunk in chunks:
                question = self.llm.invoke(
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

            unique_questions = self.llm.invoke(
                [
                    SystemMessage(
                        content=(
                            "You are a helpful assistant. Based on the list of questions provided, "
                            "generate 5 short and simple questions that together form a logical flow, starting with an introduction, "
                            "then moving to more detailed aspects, and finally concluding, as if explaining the topic in an article. "
                            "Ensure each question is clear, insightful, and in plain text only—no styling, formatting, or markdown. "
                        )
                    ),
                    HumanMessage(
                        content=f"Questions:\n{questions}\n\nPlease generate 5 logically ordered questions (introduction, details, conclusion) based on the above questions. RETURN ONLY THE QUESTION AS TEXT SEPARATED BY \"||\" SYMBOL."
                    ),
                ]
            )

            ques = unique_questions.content.split("||")
            self.aegis_questions_index.store(paper['id'], data={'questions': ques, 'status': PaperStatus.INGESTED,
                                                                'ingested_at': date.today().strftime("%Y-%m-%d")})

            self.elastic_rag.ingest_documents(chunk_texts)
            break
            # for q in ques:
            #     answer = elastic_rag.query(q)
            #     logger.info(f"Question: {q} | Answer: {answer}", extra={"job_id": str(uuid.uuid4())})


if __name__ == "__main__":
    service = HFaceResearchIngestionService()
    service.run_automtion()
    logger.info("HFace Research Ingestion Service job finished")