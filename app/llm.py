from abc import ABC, abstractmethod
from openai import AsyncOpenAI
from app.core.config import settings

class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, system: str, prompt: str) -> str:
        raise NotImplementedError

class LocalProvider(LLMProvider):
    async def complete(self, system: str, prompt: str) -> str:
        return f"[LOCAL DEMO]\n{system}\n\n{prompt[:1200]}"

class OpenAIProvider(LLMProvider):
    def __init__(self):
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required")
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def complete(self, system: str, prompt: str) -> str:
        response = await self.client.responses.create(
            model=settings.openai_model,
            instructions=system,
            input=prompt,
        )
        return response.output_text

def get_llm() -> LLMProvider:
    if settings.llm_provider.lower() == "openai":
        return OpenAIProvider()
    return LocalProvider()
