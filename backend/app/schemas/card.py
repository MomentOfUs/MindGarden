from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class KnowledgeCardBase(BaseModel):
    title: str
    content: str
    content_type: str = "markdown"
    summary: Optional[str] = ""
    tags: Optional[str] = ""
    category: Optional[str] = None
    status: str = "active"
    priority: int = 0
    is_favorite: bool = False
    is_public: bool = False


class KnowledgeCardCreate(KnowledgeCardBase):
    pass


class KnowledgeCardUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    is_favorite: Optional[bool] = None
    is_public: Optional[bool] = None


class KnowledgeCard(KnowledgeCardBase):
    id: Optional[int] = None
    owner_id: int
    created_at: datetime
    updated_at: datetime
    last_accessed: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class NotebookBase(BaseModel):
    name: str
    description: Optional[str] = ""
    color: str = "#3B82F6"
    is_default: bool = False


class NotebookCreate(NotebookBase):
    pass


class NotebookUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    is_default: Optional[bool] = None


class Notebook(NotebookBase):
    id: Optional[int] = None
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CardReferenceBase(BaseModel):
    referenced_card_id: int
    reference_type: str = "related"
    description: Optional[str] = None


class CardReferenceCreate(CardReferenceBase):
    pass


class CardReference(CardReferenceBase):
    id: Optional[int] = None
    card_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class KnowledgeCardWithReferences(KnowledgeCard):
    references: List[CardReference] = []