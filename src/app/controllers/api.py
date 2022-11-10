from typing import List

from fastapi import APIRouter, Query

from app.config import config
from app.enums import OperatorEnum
from app.services.paragraph_service import paragraph_service
from app.services.elasticsearch_service import elasticsearch_service
from app.utils import nature_language

api_router = APIRouter()


@api_router.get("/get")
async def fetch_paragraph():
    paragraph = await paragraph_service.get_paragraph(number_of_sentences=config.NUMBER_OF_SENTENCES_PER_PARAGRAPH)
    document = await elasticsearch_service.add_paragraph(paragraph)

    # Should be handled by task queue
    words_with_count = nature_language.get_distinct_words_with_count(paragraph)
    await elasticsearch_service.upsert_words_count(words_with_count)
    return document


@api_router.get("/search")
async def search_paragraphs(
        keywords: List[str] = Query(),
        operator: str = Query(default=OperatorEnum.AND),
        page: int = Query(default=1),
        per_page: int = Query(default=10)
):
    offset = (page - 1) * per_page
    result = await elasticsearch_service.search_paragraphs(keywords, operator, offset, per_page)
    return result


@api_router.get("/dictionary")
async def get_dictionary():
    top_words = await elasticsearch_service.get_top_words(count=config.TOP_WORDS_TO_RETURN_IN_DICTIONARY)
    return top_words
