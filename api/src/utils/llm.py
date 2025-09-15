import os

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from pydantic import SecretStr


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or ""
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY") or ""


def get_llm(provider: str) -> BaseChatModel:
    if provider == "openai":
        return ChatOpenAI(
            model="gpt-5",
            api_key=SecretStr(OPENAI_API_KEY),
        )
    elif provider == "anthropic":
        return ChatAnthropic(
            model='claude-4-opus-20250514',
            api_key=SecretStr(ANTHROPIC_API_KEY),
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")
