from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(
        sa_column=Column(pg.VARCHAR(255), unique=True, index=True, nullable=False)
    )
    username: str = Field(
        sa_column=Column(pg.VARCHAR(100), unique=True, index=True, nullable=False)
    )
    full_name: Optional[str] = Field(
        sa_column=Column(pg.VARCHAR(255), nullable=True)
    )
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    profile: Optional["UserProfile"] = Relationship(back_populates="user")
    cards: List["KnowledgeCard"] = Relationship(back_populates="owner")
    media: List["MediaItem"] = Relationship(back_populates="owner")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)
    bio: Optional[str] = Field(default="")
    avatar_url: Optional[str] = Field(default=None)
    location: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    theme_preference: str = Field(default="light")
    language: str = Field(default="zh-CN")
    notification_preferences: Dict[str, Any] = Field(
        default_factory=dict, 
        sa_column=Column(pg.JSON)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: Optional[User] = Relationship(back_populates="profile")