from fastapi import APIRouter

from .urls import router as urls_router
from .db_api import router as db_router

main_router = APIRouter()
main_router.include_router(urls_router, tags=['urls service'])
main_router.include_router(db_router, prefix='/db', tags=['db service'])
