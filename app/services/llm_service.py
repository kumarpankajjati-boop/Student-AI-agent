"""Core AI logic (Day 3 'service.py').

Two interchangeable models, chosen with LLM_PROVIDER in .env:
  ollama  -> local Llama 3.2, fully offline (Day 10)
  gemini  -> Google Gemini through an API key (Day 3 to 5)

Chat memory (Day 4): the last few question/answer pairs per session_id are kept in
memory and sent back to the model, so follow-up questions work.
"""
from collections import deque
from typing import Deque, Dict, Tuple

from app.config import settings
from app.logger import logger

SYSTEM_PROMPT = """
You are a helpful assistant for a school student database. Use the following
database records to answer user questions accurately and professionally.

Rules:
- Every record has these fields: ID, name, class, section, subject, age.
  You are allowed to share ALL of them.
- "Details" or "information" about a student means all fields of that student's record.
- For follow-up questions such as "them", "their" or "those students", use the students
  mentioned earlier in this chat and answer from the records.
- Count carefully when asked "how many".
- Only say that something is missing if that field really is not in the records.
"""

MAX_TURNS = 5
_history: Dict[str, Deque[Tuple[str, str]]] = {}
_llm = None


class LLMUnavailable(Exception):
    """Raised when the model cannot be reached or is not configured."""


def get_llm():
    """Create the model once and reuse it."""
    global _llm
    if _llm is not None:
        return _llm

    provider = settings.llm_provider.strip().lower()
    if provider == "gemini":
        if not settings.google_api_key:
            raise LLMUnavailable("GOOGLE_API_KEY is empty. Add it to the .env file (or the host's environment settings).")
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError as exc:
            raise LLMUnavailable("Install it with: pip install langchain-google-genai") from exc
        _llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=0.2,
        )
    else:
        from langchain_ollama import ChatOllama

        _llm = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=0.2,
        )
    logger.info("LLM ready | provider=%s", provider)
    return _llm


def _to_text(content) -> str:
    """Some models return a list of parts instead of a plain string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict) and "text" in part:
                parts.append(part["text"])
        return "".join(parts)
    return str(content)


def ask_ai(question: str, records: str, session_id: str = "default") -> str:
    history = _history.setdefault(session_id, deque(maxlen=MAX_TURNS))

    past = ""
    if history:
        past = "\nEarlier in this chat:\n" + "\n".join(f"User: {q}\nAssistant: {a}" for q, a in history) + "\n"

    prompt = f"{SYSTEM_PROMPT}\nDatabase:\n{records}\n{past}\nQuestion: {question}"

    try:
        response = get_llm().invoke(prompt)
    except LLMUnavailable:
        raise
    except Exception as exc:  # most common: ollama serve not running, or wrong Gemini model name (404)
        raise LLMUnavailable(
            f"The {settings.llm_provider} model could not answer. "
            f"For ollama check that 'ollama serve' is running; for gemini check the key and model name. ({exc})"
        ) from exc

    answer = _to_text(response.content).strip()
    history.append((question, answer))
    return answer


def reset_memory(session_id: str) -> None:
    _history.pop(session_id, None)
