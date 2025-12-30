from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class MediaItemBase(BaseModel):
    title: str
    media_type: str = "book"
    original_title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[float] = None
    personal_rating: Optional[float] = None
    status: str = "want_to_read"
    progress: float = 0.0
    notes: Optional[str] = None
    external_id: Optional[str] = None
    external_source: Optional[str] = None
    poster_url: Optional[str] = None
    metadata: Optional[dict] = {}
    tags: Optional[str] = ""
    category: Optional[str] = None


class MediaItemCreate(MediaItemBase):
    pass


class MediaItemUpdate(BaseModel):
    title: Optional[str] = None
    media_type: Optional[str] = None
    original_title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[float] = None
    personal_rating: Optional[float] = None
    status: Optional[str] = None
    progress: Optional[float] = None
    notes: Optional[str] = None
    external_id: Optional[str] = None
    external_source: Optional[str] = None
    poster_url: Optional[str] = None
    metadata: Optional[dict] = None
    tags: Optional[str] = None
    category: Optional[str] = None


class MediaItem(MediaItemBase):
    id: Optional[int] = None
    owner_id: int
    created_at: datetime
    updated_at: datetime
    last_accessed: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MediaCollectionBase(BaseModel):
    name: str
    description: Optional[str] = ""
    color: str = "#10B981"
    is_default: bool = False


class MediaCollectionCreate(MediaCollectionBase):
    pass


class MediaCollectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    is_default: Optional[bool] = None


class MediaCollection(MediaCollectionBase):
    id: Optional[int] = None
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True