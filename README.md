# AI-Powered Research Paper Processing & RAG System

A sophisticated system that combines Elasticsearch logging with automated research paper discovery, processing, and AI-powered analysis. This project has evolved beyond a simple logging utility into a comprehensive research automation tool.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [Configuration Reference](#configuration-reference)
- [Usage Guide](#usage-guide)
- [System Workflow](#system-workflow)
- [API Reference](#api-reference)
- [Testing & Development](#testing--development)
- [Production Deployment](#production-deployment)
- [Examples & Use Cases](#examples--use-cases)
- [Troubleshooting](#troubleshooting)
- [Contributing & License](#contributing--license)

## 🔍 Overview

This system automates the discovery, processing, and analysis of research papers using a combination of AI technologies and Elasticsearch. It fetches daily research papers, processes them using LLMs (Large Language Models), generates insightful questions and answers, and stores everything in a searchable Elasticsearch database with comprehensive logging.

**Key Value Proposition:**
- Automated research paper discovery and processing
- AI-powered question generation and analysis
- Retrieval Augmented Generation (RAG) for intelligent Q&A
- Comprehensive structured logging to Elasticsearch
- Modular, extensible architecture

## ✨ Key Features

### Automated Research Discovery
- Integrates with HuggingFace's daily papers API
- Automatically discovers new research papers
- Configurable filters and search criteria

### ArXiv Integration
- Downloads papers directly from ArXiv using paper IDs
- Processes PDF files to extract clean text
- Handles academic formatting and special characters

### AI-Powered Analysis
- Generates contextual questions from document chunks
- Creates structured question sets that form a logical narrative
- Produces insightful summaries and analyses

### RAG System
- Implements Retrieval Augmented Generation
- Stores document embeddings in Elasticsearch vector store
- Provides accurate, context-aware answers to questions

### Comprehensive Logging
- Structured logging to Elasticsearch
- Automatic date-based index naming
- Support for multiple authentication methods
- Console logging for development

### Modular Architecture
- Clean separation of concerns
- Extensible components
- Well-tested core functionality

## 🏗️ Architecture

The system follows a modular architecture with clear separation of concerns:

```
project_root/
├── bin/                    # Executable scripts
│   └── python_elastic_logging.py  # Main execution script
├── config/                 # Configuration management
│   ├── config.py           # Configuration loader
│   └── .env.sample         # Environment variable template
├── core/                   # AI model wrappers
│   ├── custom_completions.py  # LLM wrapper
│   ├── custom_embeddings.py   # Embedding model wrapper
│   └── tests/              # Core component tests
├── lib/                    # Core libraries
│   ├── arxiv_journal.py    # ArXiv API client
│   ├── elastic_rag.py      # RAG implementation
│   ├── hface.py            # HuggingFace API client
│   ├── logger.py           # Elasticsearch logging
│   ├── pdf_loader.py       # PDF processing
│   ├── rag_chunking.py     # Document chunking
│   └── tests/              # Library tests
└── local/                  # Local storage
    └── docs/               # Downloaded documents
```

### Data Flow

1. **Discovery**: HuggingFace client discovers new research papers
2. **Download**: ArXiv client downloads papers as PDFs
3. **Processing**: PDF loader extracts and cleans text
4. **Chunking**: Documents are split into manageable chunks
5. **Analysis**: LLM generates questions and insights
6. **Storage**: Chunks and embeddings stored in Elasticsearch
7. **Querying**: RAG system answers questions using stored context
8. **Logging**: All operations logged to Elasticsearch

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- Elasticsearch 7.x or 8.x
- OpenAI API key or compatible API (for LLM and embeddings)
- HuggingFace API token (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/preethamnagesh8/elastic_python.git
   cd elastic_python
   ```

2. Install dependencies:
   ```bash
   pip install -r req.txt
   ```

3. Create a `.env` file based on the provided `.env.sample`:
   ```bash
   cp config/.env.sample .env
   ```

4. Configure your environment variables (see [Configuration Reference](#configuration-reference))

### Elasticsearch Setup

1. Ensure Elasticsearch is running and accessible
2. Create necessary indices (the system will auto-create them if they don't exist)
3. Configure authentication (Basic Auth or API Key)

## ⚙️ Configuration Reference

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ES_HOST` | Elasticsearch host URL | Yes | - |
| `ES_INDEX` | Base index name for logs | Yes | - |
| `ES_USERNAME` | Elasticsearch username | No* | - |
| `ES_PASSWORD` | Elasticsearch password | No* | - |
| `ES_API_KEY` | Elasticsearch API key | No* | - |
| `RAG_INDEX` | Index name for RAG vectors | Yes | - |
| `OPENAI_BASE_URL` | OpenAI-compatible API URL | Yes | - |
| `OPENAI_RAG_API_SECRET` | API key for LLM/embeddings | Yes | - |
| `EMBEDDING_MODEL` | Embedding model name | Yes | text-embedding-ada-002 |
| `OPENAI_CHAT_MODEL` | Chat completion model | Yes | gpt-4 |
| `HUGGING_FACE_READ_ONLY_TOKEN` | HuggingFace API token | No | - |
| `DOWNLOAD_PATH` | Path to store downloaded papers | No | local/docs/ |

\* Either `ES_USERNAME`+`ES_PASSWORD` or `ES_API_KEY` is required

### Authentication Methods

#### Basic Authentication
```
ES_USERNAME=elastic
ES_PASSWORD=your_password
```

#### API Key Authentication
```
ES_API_KEY=your_api_key
```

### Example Configuration

```
ES_HOST=https://localhost:9200
ES_INDEX=research-logs-
ES_USERNAME=elastic
ES_PASSWORD=changeme
RAG_INDEX=research-vectors
OPENAI_BASE_URL=https://api.openai.com
OPENAI_RAG_API_SECRET=sk-...
EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_CHAT_MODEL=gpt-4
HUGGING_FACE_READ_ONLY_TOKEN=hf_...
DOWNLOAD_PATH=local/docs/
```

## 📖 Usage Guide

### Basic Usage

Run the main script to process papers and generate insights:

```bash
python bin/python_elastic_logging.py
```

### Scheduled Execution

To run the system on a schedule, uncomment the scheduling code in `python_elastic_logging.py`:

```python
# Uncomment to run every x minutes
schedule.every(x).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

### Manual Paper Processing

Process a specific paper by ID:

```python
from bin.python_elastic_logging import process_paper

arxiv_id = '2507.15846'
process_paper(arxiv_id)
```

### Querying the RAG System

Use the RAG system to answer questions about ingested papers:

```python
from lib.elastic_rag import ElasticRAG
from core.custom_embeddings import NewEmbeddings
from core.custom_completions import NewGPT
from config.config import Config
import os

# Initialize components
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

# Initialize RAG
elastic_rag = ElasticRAG(
    Config.get("ES_USERNAME"), 
    Config.get("ES_PASSWORD"),
    embedding_model, 
    llm
)

# Query the system
question = "What are the key findings of recent LLM research?"
answer = elastic_rag.query(question)
print(answer)
```

## 🔄 System Workflow

### 1. Paper Discovery
The system uses the HuggingFace API to discover daily research papers. It fetches metadata including titles, authors, and ArXiv IDs.

```python
research_papers = hface_client.get_research_papers(today_date_str)
```

### 2. Paper Download
For each discovered paper, the system downloads the PDF from ArXiv using the paper ID.

```python
paper = arxiv_client.get_paper_by_id(res_paper['paper']['id'])
arxiv_client.download_file(paper['id'], paper['pdf_url'], download_path)
```

### 3. PDF Processing
The PDF is loaded and processed to extract clean text content.

```python
pages = pdf_loader(download_path + f"{paper['id']}.pdf")
```

### 4. Document Chunking
The extracted text is split into manageable chunks for processing.

```python
chunks = chunk_documents(pages)
```

### 5. Question Generation
The LLM generates contextual questions for each chunk of text.

```python
question = llm.invoke([
    SystemMessage(content="..."),
    HumanMessage(content=f"Context:\n{chunk}\n\nPlease generate a relevant question..."),
])
```

### 6. Logical Flow Creation
The system generates a set of 5 questions that form a logical narrative flow.

```python
unique_questions = llm.invoke([
    SystemMessage(content="..."),
    HumanMessage(content=f"Questions:\n{questions}\n\nPlease generate 5 logically ordered questions..."),
])
```

### 7. Vector Storage
Document chunks are embedded and stored in Elasticsearch.

```python
elastic_rag.ingest_documents(chunk_texts)
```

### 8. Question Answering
The RAG system answers the generated questions using the stored context.

```python
for q in ques:
    answer = elastic_rag.query(q)
    logger.info(f"Question: {q} | Answer: {answer}")
```

### 9. Logging
All operations are logged to Elasticsearch with structured data.

```python
logger.info("Job started", extra={"job_id": str(uuid.uuid4())})
```

## 📚 API Reference

### Core Classes

#### ElasticsearchHandler
Custom logging handler that sends logs to Elasticsearch.

```python
handler = ElasticsearchHandler(
    hosts=[es_host],
    index=index_name,
    username=username,
    password=password
)
```

#### ElasticRAG
RAG implementation with Elasticsearch backend.

```python
rag = ElasticRAG(
    es_username,
    es_password,
    embedding_model,
    llm_model,
    chunk_size=500,
    chunk_overlap=50
)
```

#### NewGPT
Custom LLM wrapper for OpenAI-compatible APIs.

```python
llm = NewGPT(
    base_url=api_url,
    api_key=api_key,
    model=model_name
)
```

#### NewEmbeddings
Custom embedding model wrapper.

```python
embeddings = NewEmbeddings(
    base_url=api_url,
    api_key=api_key,
    model=model_name
)
```

#### ArxivClient
Client for interacting with ArXiv API.

```python
client = ArxivClient()
paper = client.get_paper_by_id(arxiv_id)
```

#### HuggingFaceClient
Client for interacting with HuggingFace API.

```python
client = HuggingFaceClient(api_token)
papers = client.get_research_papers(date_str)
```

## 🧪 Testing & Development

### Running Tests

Run tests for the logger:

```bash
python -m unittest lib.tests.test_logger
```

Run tests for the custom completions:

```bash
python -m unittest core.tests.test_custom_completions
```

### Development Setup

1. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -r req.txt
   ```

3. Configure a local Elasticsearch instance for testing

### Adding New Features

1. Follow the modular architecture
2. Add appropriate tests
3. Update documentation
4. Ensure backward compatibility

## 🌐 Production Deployment

### Security Considerations

- Always use `verify_certs=True` in production
- Use API keys with limited permissions
- Rotate credentials regularly
- Use HTTPS for all connections

### Performance Optimization

- Adjust chunk size and overlap for optimal RAG performance
- Consider batch processing for large document sets
- Use appropriate Elasticsearch index settings for vector search

### Monitoring and Alerting

- Set up Elasticsearch monitoring
- Configure alerts for failed jobs
- Monitor API rate limits

### Scaling Considerations

- Use Elasticsearch cluster for high availability
- Consider distributed processing for large document volumes
- Implement caching for frequently accessed embeddings

## 📝 Examples & Use Cases

### Research Team Automation

Automatically process and analyze new research papers in your field:

```python
# Configure for specific research domains
hface_client = HuggingFaceClient(token)
papers = hface_client.get_research_papers_by_category("machine-learning")

# Process each paper
for paper in papers:
    process_paper(paper['id'])
```

### Literature Review Assistant

Generate comprehensive literature reviews:

```python
# Process multiple papers
paper_ids = ['2507.15846', '2507.15847', '2507.15848']
for paper_id in paper_ids:
    process_paper(paper_id)

# Generate literature review
review_question = "What are the common themes and differences in these papers?"
review = elastic_rag.query(review_question)
```

### Research Question Exploration

Explore specific research questions across papers:

```python
questions = [
    "How do these papers address model efficiency?",
    "What evaluation metrics are commonly used?",
    "What are the limitations mentioned in these studies?"
]

for question in questions:
    answer = elastic_rag.query(question)
    print(f"Q: {question}\nA: {answer}\n")
```

## 🔧 Troubleshooting

### Common Issues

#### Elasticsearch Connection Problems

**Issue**: Cannot connect to Elasticsearch
**Solution**: 
- Verify Elasticsearch is running
- Check network connectivity
- Ensure authentication credentials are correct
- Verify SSL/TLS configuration

#### API Authentication Issues

**Issue**: API key authentication failures
**Solution**:
- Verify API keys are valid and not expired
- Check for proper environment variable configuration
- Ensure API endpoints are correct

#### PDF Processing Errors

**Issue**: Failed to extract text from PDFs
**Solution**:
- Verify PDF is not corrupted
- Check if PDF is password protected
- Try alternative PDF processing libraries

#### Vector Search Performance

**Issue**: Slow vector search performance
**Solution**:
- Optimize Elasticsearch index settings
- Adjust chunk size and overlap
- Consider using approximate nearest neighbor search

## 🤝 Contributing & License

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Built with ❤️ by [Preetham Nagesh](https://github.com/preethamnagesh8)
