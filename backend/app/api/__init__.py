from fastapi import APIRouter
from app.api.v1 import auth, cards, media

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(cards.router, prefix="/library", tags=["knowledge-cards"])
api_router.include_router(media.router, prefix="/media", tags=["media-items"])