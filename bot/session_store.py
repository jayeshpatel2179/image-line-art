"""In-memory per-chat session state.

Single-process only — swap for Redis (or similar) if you ever run more than one bot
instance, since this dict is not shared across processes.
"""

_sessions: dict[int, dict] = {}


def set_pending_prompt(chat_id: int, raw_text: str, final_prompt: str) -> None:
    _sessions[chat_id] = {"raw_text": raw_text, "final_prompt": final_prompt}


def get_session(chat_id: int) -> dict | None:
    return _sessions.get(chat_id)


def clear_session(chat_id: int) -> None:
    _sessions.pop(chat_id, None)
