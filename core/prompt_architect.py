"""Stage A: turns one line of user text into a text-free house-style scene prompt."""

from openai import AsyncOpenAI

from config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def build_scene_prompt(user_text: str) -> str:
    response = await client.chat.completions.create(
        model=settings.TEXT_MODEL,
        messages=[
            {"role": "system", "content": settings.MASTER_PROMPT},
            {"role": "user", "content": user_text.strip()},
        ],
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()
