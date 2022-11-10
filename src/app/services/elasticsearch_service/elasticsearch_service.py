from datetime import datetime
from typing import List
from uuid import uuid4

from elasticsearch import AsyncElasticsearch

from app.config import config
from app.enums import OperatorEnum

es_client = AsyncElasticsearch(
    config.ELASTICSEARCH_HOST,
    basic_auth=(config.ELASTICSEARCH_USERNAME, config.ELASTICSEARCH_PASSWORD),
    verify_certs=False,
)


async def add_paragraph(paragraph: str):
    document = {
        "id": str(uuid4()),
        "content": paragraph,
        "created": datetime.utcnow()
    }
    await es_client.index(index=config.ELASTICSEARCH_PARAGRAPHS_INDEX, document=document)
    return document


async def search_paragraphs(keywords: List[str], operator: str, offset: int):
    pass


async def get_top_words(count: int):
    pass
