from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from app.models.user import User


class KnowledgeCard(SQLModel, table=True):
    __tablename__ = "knowledge_cards"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(
        sa_column=Column(pg.VARCHAR(500), nullable=False, index=True)
    )
    content: str = Field(sa_column=Column(pg.TEXT, nullable=False))
    content_type: str = Field(default="markdown")
    summary: Optional[str] = Field(default="")
    tags: Optional[str] = Field(
        sa_column=Column(pg.VARCHAR(1000), nullable=True)
    )
    category: Optional[str] = Field(
        sa_column=Column(pg.VARCHAR(100), index=True, nullable=True)
    )
    status: str = Field(default="active")
    priority: int = Field(default=0)
    is_favorite: bool = Field(default=False)
    is_public: bool = Field(default=False)
    
    owner_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: Optional[datetime] = None
    
    owner: Optional[User] = Relationship(back_populates="cards")
    references: List["CardReference"] = Relationship(back_populates="card", foreign_keys="CardReference.card_id")
    
    def __repr__(self) -> str:
        return f"<KnowledgeCard(id={self.id}, title='{self.title[:50]}...', owner_id={self.owner_id})>"


class Notebook(SQLModel, table=True):
    __tablename__ = "notebooks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(
        sa_column=Column(pg.VARCHAR(200), nullable=False, index=True)
    )
    description: Optional[str] = Field(default="")
    color: str = Field(default="#3B82F6")
    is_default: bool = Field(default=False)
    
    owner_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    cards: List[KnowledgeCard] = Relationship()
    
    def __repr__(self) -> str:
        return f"<Notebook(id={self.id}, name='{self.name}', owner_id={self.owner_id})>"


class CardReference(SQLModel, table=True):
    __tablename__ = "card_references"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    card_id: int = Field(foreign_key="knowledge_cards.id", index=True)
    referenced_card_id: int = Field(foreign_key="knowledge_cards.id", index=True)
    reference_type: str = Field(default="related")
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    card: Optional[KnowledgeCard] = Relationship(back_populates="references", foreign_keys="CardReference.card_id")
    
    def __repr__(self) -> str:
        return f"<CardReference(id={self.id}, card_id={self.card_id}, referenced_card_id={self.referenced_card_id})>"