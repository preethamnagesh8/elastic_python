import os
import unittest
from unittest.mock import patch, MagicMock
from langchain_core.messages import BaseMessage, AIMessage

from core.custom_completions import NewGPT

class TestNewGPT(unittest.TestCase):
    def setUp(self):
        self.gpt = NewGPT(
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("OPENAI_RAG_API_SECRET"),
            model=os.getenv("OPENAI_CHAT_MODEL"),
        )

    def test_convert_messages_to_openai_format(self):
        messages = [
            BaseMessage(type="human", content="Hello!"),
            BaseMessage(type="ai", content="Hi there!"),
            BaseMessage(type="system", content="System message."),
        ]
        formatted = self.gpt._convert_messages_to_openai_format(messages)
        self.assertEqual(formatted, [
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "system", "content": "System message."},
        ])

    @patch("core.custom_completions.requests.post")
    def test_generate_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        mock_post.return_value = mock_response

        messages = [BaseMessage(type="human", content="Say hi")]
        result = self.gpt._generate(messages)
        self.assertEqual(result.generations[0].message.content, "Test response")

    def test_convert_messages_to_openai_format_invalid_type(self):
        messages = [BaseMessage(type="unknown", content="???")]
        with self.assertRaises(ValueError):
            self.gpt._convert_messages_to_openai_format(messages)

if __name__ == "__main__":
    unittest.main()