from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import ElasticsearchStore
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.schema import Document
from langchain_core.embeddings import Embeddings
from elasticsearch import Elasticsearch

from config.config import Config


class ElasticRAG:
    def __init__(
        self,
        es_username: str,
        es_password,
        embedding_model: Optional[Embeddings] = None,  # Accepts any embedding model
        llm_model: Optional[OpenAI] = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        self.index_name = Config.get("RAG_INDEX")
        self.embedding_model = embedding_model
        self.llm_model = llm_model or OpenAI(temperature=0)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vectorstore = None
        self.qa_chain = None
        self.es_client = Elasticsearch(
            [Config.get("ES_HOST")],
            basic_auth=(es_username, es_password),
            verify_certs=False
        )

    def ingest_documents(self, documents: List[str]):
        """
        Ingest raw text documents (list of strings),
        chunk them and create Elasticsearch vector store.
        """
        if self.embedding_model is None:
            raise ValueError("An embedding model must be provided.")

        # Convert strings to LangChain Document objects
        docs = [Document(page_content=d) for d in documents]

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        split_docs = text_splitter.split_documents(docs)

        # Create Elasticsearch vector store
        self.vectorstore = ElasticsearchStore.from_documents(
            split_docs,
            embedding=self.embedding_model,
            index_name=self.index_name,
            es_connection=self.es_client,
        )

        # Create RetrievalQA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm_model, retriever=self.vectorstore.as_retriever()
        )

    def ingest_from_loader(self, loader):
        """
        Ingest documents from a LangChain Document Loader
        """
        docs = loader.load()
        self.ingest_documents([doc.page_content for doc in docs])

    def query(self, question: str) -> str:
        """
        Query the RAG system with a question string.
        """
        if not self.qa_chain:
            raise ValueError("No documents ingested. Please call ingest_documents first.")
        return self.qa_chain.run(question)