"""LLM provider implementation.

Implement the LLMProvider Protocol defined in::

    domain/interfaces.py → class LLMProvider(Protocol)

Required methods:
    async def generate(self, messages: list[Message]) -> str
    async def stream(self, messages: list[Message]) -> AsyncIterator[str]

Conventions:
    - All connection config (api_key, model name, endpoint) comes from
      config.py (Settings). Never hardcode credentials here.
    - Catch SDK-specific exceptions and re-raise as domain exceptions::

        from {{ cookiecutter.project_slug }}.domain.exceptions import GenerationError, RateLimitError

        try:
            response = await client.messages.create(...)
        except SomeSDKRateLimitError as exc:
            raise RateLimitError("Rate limit hit") from exc
        except SomeSDKError as exc:
            raise GenerationError("Generation failed") from exc

    - This file is NEVER imported directly by application/.
      Injection happens in infrastructure/api/dependencies.py (or equivalent).
    - When you pick your provider, rename this file for clarity:
        anthropic_llm.py, gemini_llm.py, openai_llm.py, ollama_llm.py, etc.

Examples of providers you could implement:
    - Claude (Anthropic SDK: pip install anthropic)
    - Gemini (Vertex AI SDK: pip install google-cloud-aiplatform)
    - GPT-4 / any OpenAI-compatible endpoint (pip install openai)
    - Local models via Ollama (pip install ollama)
"""

from typing import AsyncIterator

from {{ cookiecutter.project_slug }}.config import settings
from {{ cookiecutter.project_slug }}.domain.models import Message

# TODO: Install your chosen SDK and import it here.
# Example: from anthropic import AsyncAnthropic


class LLMProvider:
    """Concrete implementation of the LLMProvider Protocol.

    Replace the body of generate() and stream() with calls to your
    chosen SDK. The interface contract is defined in domain/interfaces.py.

    Args:
        model: The model identifier to use for generation.
            Defaults to the value in settings.llm_model.
    """

    def __init__(self, model: str | None = None) -> None:
        self.model = model or settings.llm_model
        # TODO: Initialize your SDK client here.
        # Example: self._client = AsyncAnthropic(api_key=settings.llm_api_key)

    async def generate(self, messages: list[Message]) -> str:
        """Generate a complete response.

        Args:
            messages: Conversation history including the current user message.

        Returns:
            The model's response as a plain string.

        Raises:
            GenerationError: If the SDK call fails.
            RateLimitError: If the provider's rate limit is exceeded.
        """
        # TODO: Call your SDK here and return the response text.
        # Example (Anthropic):
        #
        #   sdk_messages = [{"role": m.role, "content": m.content} for m in messages]
        #   response = await self._client.messages.create(
        #       model=self.model,
        #       max_tokens=1024,
        #       messages=sdk_messages,
        #   )
        #   return response.content[0].text
        raise NotImplementedError("Implement generate() with your chosen LLM SDK.")

    async def stream(self, messages: list[Message]) -> AsyncIterator[str]:
        """Stream a response token by token.

        Args:
            messages: Conversation history including the current user message.

        Yields:
            Individual tokens or chunks as they are generated.

        Raises:
            GenerationError: If the stream fails mid-way.
        """
        # TODO: Call your SDK's streaming API here.
        # Example (Anthropic):
        #
        #   sdk_messages = [{"role": m.role, "content": m.content} for m in messages]
        #   async with self._client.messages.stream(
        #       model=self.model,
        #       max_tokens=1024,
        #       messages=sdk_messages,
        #   ) as stream:
        #       async for text in stream.text_stream:
        #           yield text
        raise NotImplementedError("Implement stream() with your chosen LLM SDK.")
        yield  # Make this a generator even before implementation
