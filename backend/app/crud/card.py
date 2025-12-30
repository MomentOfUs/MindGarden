from typing import List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, update
from sqlalchemy.orm import selectinload
from app.models.card import KnowledgeCard, Notebook, CardReference
from app.schemas.card import KnowledgeCardCreate, KnowledgeCardUpdate, NotebookCreate, NotebookUpdate
from app.core.utils import normalize_tags, paginate_results


class KnowledgeCardCRUD:
    async def get_by_id(self, db: AsyncSession, *, id: int) -> Optional[KnowledgeCard]:
        result = await db.execute(
            select(KnowledgeCard)
            .options(selectinload(KnowledgeCard.references))
            .where(KnowledgeCard.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        owner_id: int, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[str] = None,
        tags: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[KnowledgeCard]:
        query = select(KnowledgeCard).where(KnowledgeCard.owner_id == owner_id)
        
        if category:
            query = query.where(KnowledgeCard.category == category)
        
        if status:
            query = query.where(KnowledgeCard.status == status)
        
        if tags:
            normalized_tags = normalize_tags(tags)
            for tag in normalized_tags:
                query = query.where(KnowledgeCard.tags.like(f"%{tag}%"))
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    KnowledgeCard.title.like(search_term),
                    KnowledgeCard.content.like(search_term),
                    KnowledgeCard.summary.like(search_term)
                )
            )
        
        query = query.offset(skip).limit(limit).order_by(KnowledgeCard.updated_at.desc())
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, *, obj_in: KnowledgeCardCreate, owner_id: int) -> KnowledgeCard:
        db_obj = KnowledgeCard(**obj_in.dict(), owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, *, db_obj: KnowledgeCard, obj_in: KnowledgeCardUpdate) -> KnowledgeCard:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, *, id: int, owner_id: int) -> bool:
        card = await self.get_by_id(db, id=id)
        if card and card.owner_id == owner_id:
            await db.delete(card)
            await db.commit()
            return True
        return False
    
    async def get_favorites(self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[KnowledgeCard]:
        result = await db.execute(
            select(KnowledgeCard)
            .where(and_(KnowledgeCard.owner_id == owner_id, KnowledgeCard.is_favorite == True))
            .offset(skip)
            .limit(limit)
            .order_by(KnowledgeCard.updated_at.desc())
        )
        return result.scalars().all()
    
    async def get_recent(self, db: AsyncSession, *, owner_id: int, limit: int = 10) -> List[KnowledgeCard]:
        result = await db.execute(
            select(KnowledgeCard)
            .where(KnowledgeCard.owner_id == owner_id)
            .order_by(KnowledgeCard.updated_at.desc())
            .limit(limit)
        )
        return result.scalars().all()


class NotebookCRUD:
    async def get_by_id(self, db: AsyncSession, *, id: int) -> Optional[Notebook]:
        result = await db.execute(select(Notebook).where(Notebook.id == id))
        return result.scalar_one_or_none()
    
    async def get_multi(self, db: AsyncSession, *, owner_id: int) -> List[Notebook]:
        result = await db.execute(
            select(Notebook)
            .where(Notebook.owner_id == owner_id)
            .order_by(Notebook.is_default.desc(), Notebook.name.asc())
        )
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, *, obj_in: NotebookCreate, owner_id: int) -> Notebook:
        await db.execute(
            update(Notebook)
            .where(and_(Notebook.owner_id == owner_id, Notebook.is_default == True))
            .values(is_default=False)
        )
        
        db_obj = Notebook(**obj_in.dict(), owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, *, db_obj: Notebook, obj_in: NotebookUpdate) -> Notebook:
        update_data = obj_in.dict(exclude_unset=True)
        
        if obj_in.is_default:
            await db.execute(
                update(Notebook)
                .where(and_(Notebook.owner_id == db_obj.owner_id, Notebook.is_default == True))
                .values(is_default=False)
            )
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, *, id: int, owner_id: int) -> bool:
        notebook = await self.get_by_id(db, id=id)
        if notebook and notebook.owner_id == owner_id:
            await db.delete(notebook)
            await db.commit()
            return True
        return False
    
    async def get_default(self, db: AsyncSession, *, owner_id: int) -> Optional[Notebook]:
        result = await db.execute(
            select(Notebook)
            .where(and_(Notebook.owner_id == owner_id, Notebook.is_default == True))
        )
        return result.scalar_one_or_none()


class CardReferenceCRUD:
    async def create(self, db: AsyncSession, *, card_id: int, referenced_card_id: int, reference_type: str = "related", description: Optional[str] = None) -> CardReference:
        db_obj = CardReference(
            card_id=card_id,
            referenced_card_id=referenced_card_id,
            reference_type=reference_type,
            description=description
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_by_card_id(self, db: AsyncSession, *, card_id: int) -> List[CardReference]:
        result = await db.execute(select(CardReference).where(CardReference.card_id == card_id))
        return result.scalars().all()
    
    async def delete(self, db: AsyncSession, *, id: int) -> bool:
        reference = await db.execute(select(CardReference).where(CardReference.id == id))
        ref_obj = reference.scalar_one_or_none()
        if ref_obj:
            await db.delete(ref_obj)
            await db.commit()
            return True
        return False


knowledge_card_crud = KnowledgeCardCRUD()
notebook_crud = NotebookCRUD()
card_reference_crud = CardReferenceCRUD()