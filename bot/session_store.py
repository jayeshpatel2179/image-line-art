"""In-memory per-chat session state.

Single-process only — swap for Redis (or similar) if you ever run more than one bot
instance, since this dict is not shared across processes.
"""

_sessions: dict[int, dict] = {}


def set_scene_prompt(chat_id: int, raw_text: str, scene_prompt: str) -> None:
    _sessions[chat_id] = {
        "raw_text": raw_text,
        "scene_prompt": scene_prompt,
        "placement": None,
        "image_path": None,
        "has_text": False,
    }


def set_placement(chat_id: int, placement: str) -> None:
    session = _sessions.get(chat_id)
    if session is not None:
        session["placement"] = placement


def set_current_image(chat_id: int, image_path) -> None:
    session = _sessions.get(chat_id)
    if session is not None:
        session["image_path"] = image_path


def set_has_text(chat_id: int, has_text: bool) -> None:
    session = _sessions.get(chat_id)
    if session is not None:
        session["has_text"] = has_text


def get_session(chat_id: int) -> dict | None:
    return _sessions.get(chat_id)


def clear_session(chat_id: int) -> None:
    _sessions.pop(chat_id, None)
