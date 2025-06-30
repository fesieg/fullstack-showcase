from fastapi import APIRouter

from app.api.endpoints.bottles_endpoint import bottle_router

api_router = APIRouter(prefix="/api")

api_router.include_router(bottle_router, tags=["bottles"])
