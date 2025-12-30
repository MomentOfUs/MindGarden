from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from .user import User


class MediaItem(SQLModel, table=True):
    __tablename__ = "media_items"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(
        sa_column=Column(pg.VARCHAR(500), nullable=False, index=True)
    )
    media_type: str = Field(default="book")
    original_title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[float] = Field(default=None)
    personal_rating: Optional[float] = Field(default=None)
    status: str = Field(default="want_to_read")
    progress: float = Field(default=0.0)
    notes: Optional[str] = None
    
    external_id: Optional[str] = None
    external_source: Optional[str] = None
    poster_url: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)
    
    tags: Optional[str] = Field(
        sa_column=Column(pg.VARCHAR(1000), nullable=True)
    )
    category: Optional[str] = Field(
        sa_column=Column(pg.VARCHAR(100), index=True, nullable=True)
    )
    
    owner_id: int = Field(foreign_key="users.id", index=True)
    owner: Optional[User] = Relationship(back_populates="media")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: Optional[datetime] = None
    
    def __repr__(self) -> str:
        return f"<MediaItem(id={self.id}, title='{self.title[:50]}...', type='{self.media_type}', owner_id={self.owner_id})>"


class MediaCollection(SQLModel, table=True):
    __tablename__ = "media_collections"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(
        sa_column=Column(pg.VARCHAR(200), nullable=False, index=True)
    )
    description: Optional[str] = Field(default="")
    color: str = Field(default="#10B981")
    is_default: bool = Field(default=False)
    
    owner_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    media_items: List[MediaItem] = Relationship()
    
    def __repr__(self) -> str:
        return f"<MediaCollection(id={self.id}, name='{self.name}', owner_id={self.owner_id})>"