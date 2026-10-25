import logging
import os
import threading
import time
from collections import deque
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator

from bft_ai.gemini_service import (
    GeminiEmptyResponseError,
    GeminiNotConfiguredError,
    GeminiRequestError,
    generate_reply,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("bft_ai.api")

RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_REQUESTS = 8
MAX_RATE_LIMIT_CLIENTS = 4096
_client_requests: dict[str, deque[float]] = {}
_rate_limit_lock = threading.Lock()

app = FastAPI(
    title="BFT Public AI Assistant",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1200)

    @field_validator("message")
    @classmethod
    def strip_message(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Question must not be blank.")
        return value


class ChatResponse(BaseModel):
    answer: str


def _check_rate_limit(client_id: str, now: float) -> bool:
    with _rate_limit_lock:
        if len(_client_requests) >= MAX_RATE_LIMIT_CLIENTS:
            expired = [
                key
                for key, events in _client_requests.items()
                if not events or now - events[-1] >= RATE_LIMIT_WINDOW_SECONDS
            ]
            for key in expired:
                _client_requests.pop(key, None)
            if len(_client_requests) >= MAX_RATE_LIMIT_CLIENTS and client_id not in _client_requests:
                return False

        events = _client_requests.setdefault(client_id, deque())
        while events and now - events[0] >= RATE_LIMIT_WINDOW_SECONDS:
            events.popleft()
        if len(events) >= RATE_LIMIT_REQUESTS:
            return False
        events.append(now)
        return True


@app.get("/", include_in_schema=False)
def website() -> FileResponse:
    deployed_page = PROJECT_ROOT / "BFT Nelson.html"
    local_page = PROJECT_ROOT / "BFT.html"
    return FileResponse(deployed_page if deployed_page.is_file() else local_page)


@app.post("/api/v1/ai/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, request: Request) -> ChatResponse:
    client_id = request.client.host if request.client else "unknown"
    if not _check_rate_limit(client_id, time.monotonic()):
        raise HTTPException(
            status_code=429,
            detail="Too many questions. Please wait a minute and try again.",
            headers={"Retry-After": str(RATE_LIMIT_WINDOW_SECONDS)},
        )

    try:
        return ChatResponse(answer=generate_reply(payload.message.strip()))
    except GeminiNotConfiguredError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except GeminiEmptyResponseError as error:
        logger.warning("Gemini returned an empty answer")
        raise HTTPException(
            status_code=502,
            detail="The AI service returned no answer. Please try again later.",
        ) from error
    except GeminiRequestError as error:
        logger.warning("Gemini request failed")
        raise HTTPException(
            status_code=502,
            detail="The AI service could not answer right now. Please try again later.",
        ) from error
