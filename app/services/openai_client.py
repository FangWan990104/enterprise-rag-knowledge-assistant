"""Shared, lazily-constructed OpenAI client."""
from __future__ import annotations

from functools import lru_cache

from openai import OpenAI

from app.config import get_settings


@lru_cache
def get_client() -> OpenAI:
    settings = get_settings()
    kwargs = {"api_key": settings.openai_api_key}
    if settings.openai_base_url:
        kwargs["base_url"] = settings.openai_base_url
    kwargs["timeout"] = 60.0
    kwargs["max_retries"] = 1
    return OpenAI(**kwargs)


@lru_cache
def get_embedding_client() -> OpenAI:
    settings = get_settings()
    return OpenAI(api_key=settings.siliconflow_api_key, base_url=settings.siliconflow_base_url)
