import unittest
from unittest.mock import patch, MagicMock
from lib.logger import get_logger
from datetime import datetime, UTC


class TestElasticLogger(unittest.TestCase):

    @patch("lib.logger.Elasticsearch")  # 👈 Patch the ES client constructor
    def test_elasticsearch_logging(self, mock_es_class):
        # Mock ES client instance and its .index() method
        mock_es = MagicMock()
        mock_es_class.return_value = mock_es

        logger = get_logger()
        logger.info("Test log message")

        self.assertTrue(mock_es.index.called)
        args, kwargs = mock_es.index.call_args

        self.assertIn("index", kwargs)
        today = datetime.now(UTC).strftime("%Y.%m.%d")
        self.assertEqual(kwargs["index"], f"elastic-test-{today}")  # or your ES_INDEX

    @patch("lib.logger.Elasticsearch")
    def test_logger_has_handlers(self, mock_es_class):
        logger = get_logger()
        self.assertGreater(len(logger.handlers), 0)

if __name__ == "__main__":
    # unittest.main()
    logger = get_logger()
    logger.info("Test log message")