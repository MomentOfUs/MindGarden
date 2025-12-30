from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from .user import User, UserCreate, UserUpdate, UserInDB, UserProfile, UserProfileCreate, UserProfileUpdate
from .card import KnowledgeCard, KnowledgeCardCreate, KnowledgeCardUpdate, Notebook, NotebookCreate, NotebookUpdate, CardReference, CardReferenceCreate, KnowledgeCardWithReferences
from .media import MediaItem, MediaItemCreate, MediaItemUpdate, MediaCollection, MediaCollectionCreate, MediaCollectionUpdate

# Add Token schema
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

__all__ = [
    "User", "UserCreate", "UserUpdate", "UserInDB",
    "UserProfile", "UserProfileCreate", "UserProfileUpdate",
    "KnowledgeCard", "KnowledgeCardCreate", "KnowledgeCardUpdate", "KnowledgeCardWithReferences",
    "Notebook", "NotebookCreate", "NotebookUpdate", 
    "CardReference", "CardReferenceCreate",
    "MediaItem", "MediaItemCreate", "MediaItemUpdate",
    "MediaCollection", "MediaCollectionCreate", "MediaCollectionUpdate",
    "Token"
]