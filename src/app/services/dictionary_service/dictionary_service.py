from typing import Optional

import httpx

from app.config import config


async def get_definition(word: str) -> Optional[str]:
    async with httpx.AsyncClient() as client:
        api_url = f"{config.DICTIONARY_API_URL}/{word}"
        response = await client.get(api_url)

        if response.status_code != 200:
            return None

        response_body = response.json()
        if not response_body:
            return None

        word_data = response_body[0]
        for meaning in word_data["meanings"]:
            for definition in meaning["definitions"]:
                return definition["definition"]

    return None
