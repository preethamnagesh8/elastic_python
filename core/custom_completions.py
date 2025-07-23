from typing import List, Optional, Any
import requests
from langchain_core.callbacks import CallbackManagerForLLMRun

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from pydantic import BaseModel, Field


class NewGPT(BaseChatModel):
    base_url: str = Field(..., description="The base URL of the LLM API")
    api_key: str = Field(..., description="The API key for authentication")
    model: str = Field("gpt-4", description="The model name to use")

    @property
    def _llm_type(self) -> str:
        return "new-gpt"

    def _convert_messages_to_openai_format(
        self, messages: List[BaseMessage]
    ) -> List[dict]:
        role_mapping = {
            "human": "user",
            "ai": "assistant",
            "system": "system",
            "function": "function",
            "tool": "tool",
            "developer": "developer",
        }

        formatted = []
        for msg in messages:
            role = role_mapping.get(msg.type)
            if not role:
                raise ValueError(f"Unsupported message type: {msg.type}")
            formatted.append({"role": role, "content": msg.content})
        return formatted

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        payload = {
            "model": self.model,
            "messages": self._convert_messages_to_openai_format(messages),
        }
        if stop:
            payload["stop"] = stop

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        url = f"{self.base_url}/v1/chat/completions"
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=content))]
        )