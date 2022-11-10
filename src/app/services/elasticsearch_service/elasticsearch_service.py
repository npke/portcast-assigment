from datetime import datetime
from typing import List
from uuid import uuid4

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

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


async def search_paragraphs(keywords: List[str], operator: str, offset: int, limit: int):
    query = {"bool": {}}

    if operator == OperatorEnum.AND:
        query["bool"]["must"] = [
            {"term": {"content": keyword}}
            for keyword in keywords
        ]
    else:
        query["bool"]["should"] = [
            {"term": {"content": keyword}}
            for keyword in keywords
        ]

    result = await es_client.search(
        index=config.ELASTICSEARCH_PARAGRAPHS_INDEX,
        body={"query": query},
        from_=offset,
        size=limit,
    )
    return {
        "total": result["hits"]["total"]["value"],
        "items": [item["_source"] for item in result["hits"]["hits"]]
    }


async def get_top_words(count: int):
    query = {
        "match_all": {}
    }
    result = await es_client.search(
        index=config.ELASTICSEARCH_WORDS_INDEX,
        body={"query": query},
        sort=[{"count": "desc"}],
        size=count
    )
    return [item["_source"] for item in result["hits"]["hits"]]


async def upsert_words_count(words_with_count):
    upserts = [
        {
            "_index": config.ELASTICSEARCH_WORDS_INDEX,
            "_id": word,
            "_op_type": "update",
            "script": {
                "source": "ctx._source.count += params.count",
                "lang": "painless",
                "params": {"count": count}
            },
            "upsert": {
                "word": word,
                "count": count,
                "definition": None,
            }
        }
        for word, count in words_with_count.items()
    ]

    await async_bulk(es_client, upserts)
