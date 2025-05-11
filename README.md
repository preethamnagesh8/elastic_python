Python Elasticsearch Logger

A lightweight, reusable Python logging utility that logs structured log messages to an Elasticsearch cluster — with support for authentication, dynamic index naming, and environment-based configuration.

--------------------------------------------------

Features:

- Logs to Elasticsearch using the official elasticsearch Python client  
- Appends current UTC date to index names (e.g., app-logs-2025.05.10)  
- Supports Basic Auth and API Key authentication  
- Optional TLS certificate verification (for secure environments)  
- Console logging fallback  
- Environment-based configuration via .env  

--------------------------------------------------

Project Structure:

project_root/
├── lib/
│   └── logger.py          -> Logging logic  
├── config/
│   └── config.py          -> Loads config from .env  
├── test_logger.py         -> Sample test with mocks  
├── .env                   -> Your secrets (not committed)  
├── requirements.txt  
└── README.txt

--------------------------------------------------

Setup:

1. Install Dependencies

   pip install -r requirements.txt

   Or manually:

   pip install elasticsearch python-dotenv

2. Create a `.env` file

Example .env content:

   ES_HOST=https://your-es-host:9200  
   ES_INDEX=app-logs  
   ES_USERNAME=elastic  
   ES_PASSWORD=your_password  
   # OR, if using API key  
   # ES_API_KEY=your_api_key

--------------------------------------------------

Run the Example:

   from lib.logger import get_logger

   logger = get_logger()
   logger.info("Application started")
   logger.error("Something failed")

--------------------------------------------------

Example Log Entry Sent to Elasticsearch:

{
  "@timestamp": "2025-05-10T03:15:12.123Z",
  "level": "INFO",
  "message": "Application started",
  "host": "your-machine-name",
  "module": "main",
  "line": 12,
  "func": "startup",
  "logger": "app_logger"
}

--------------------------------------------------

Security Notes:

- In development, verify_certs=False disables SSL validation  
- In production, always set verify_certs=True and use a valid CA certificate  

--------------------------------------------------

Testing:

   pytest test_logger.py

Tests include mock-based validation for Elasticsearch .index() calls.

--------------------------------------------------

Future Improvements:

- Add support for structured logging with structlog  
- JSON log formatting  
- OpenTelemetry integration  

--------------------------------------------------

License:

MIT License — use freely and modify as needed.
