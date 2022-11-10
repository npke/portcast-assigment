from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/get")
async def fetch_paragraph():
    pass


@api_router.get("/search")
async def search_paragraphs():
    pass


@api_router.get("/dictionary")
async def get_dictionary():
    pass
