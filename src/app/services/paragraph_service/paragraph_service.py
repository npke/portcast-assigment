import httpx

from app.config import config


async def get_paragraph(number_of_sentences: int) -> str:
    async with httpx.AsyncClient() as client:
        api_url = f"{config.METAPHORPSUM_API_URL}/sentences/{number_of_sentences}"
        response = await client.get(api_url)
        return response.text
