from typing import List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, case
from sqlalchemy.orm import selectinload
from models.media import MediaItem, MediaCollection
from schemas.media import MediaItemCreate, MediaItemUpdate, MediaCollectionCreate, MediaCollectionUpdate
from core.utils import normalize_tags, paginate_results


class MediaItemCRUD:
    async def get_by_id(self, db: AsyncSession, *, id: int) -> Optional[MediaItem]:
        result = await db.execute(select(MediaItem).where(MediaItem.id == id))
        return result.scalar_one_or_none()
    
    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        owner_id: int, 
        skip: int = 0, 
        limit: int = 100,
        media_type: Optional[str] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[MediaItem]:
        query = select(MediaItem).where(MediaItem.owner_id == owner_id)
        
        if media_type:
            query = query.where(MediaItem.media_type == media_type)
        
        if status:
            query = query.where(MediaItem.status == status)
        
        if category:
            query = query.where(MediaItem.category == category)
        
        if tags:
            normalized_tags = normalize_tags(tags)
            for tag in normalized_tags:
                query = query.where(MediaItem.tags.like(f"%{tag}%"))
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    MediaItem.title.like(search_term),
                    MediaItem.original_title.like(search_term),
                    MediaItem.description.like(search_term),
                    MediaItem.content.like(search_term)
                )
            )
        
        query = query.offset(skip).limit(limit).order_by(MediaItem.updated_at.desc())
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, *, obj_in: MediaItemCreate, owner_id: int) -> MediaItem:
        db_obj = MediaItem(**obj_in.dict(), owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, *, db_obj: MediaItem, obj_in: MediaItemUpdate) -> MediaItem:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, *, id: int, owner_id: int) -> bool:
        media = await self.get_by_id(db, id=id)
        if media and media.owner_id == owner_id:
            await db.delete(media)
            await db.commit()
            return True
        return False
    
    async def get_by_status(self, db: AsyncSession, *, owner_id: int, status: str) -> List[MediaItem]:
        result = await db.execute(
            select(MediaItem)
            .where(and_(MediaItem.owner_id == owner_id, MediaItem.status == status))
            .order_by(MediaItem.updated_at.desc())
        )
        return result.scalars().all()
    
    async def get_by_type(self, db: AsyncSession, *, owner_id: int, media_type: str) -> List[MediaItem]:
        result = await db.execute(
            select(MediaItem)
            .where(and_(MediaItem.owner_id == owner_id, MediaItem.media_type == media_type))
            .order_by(MediaItem.updated_at.desc())
        )
        return result.scalars().all()
    
    async def get_recent(self, db: AsyncSession, *, owner_id: int, limit: int = 10) -> List[MediaItem]:
        result = await db.execute(
            select(MediaItem)
            .where(MediaItem.owner_id == owner_id)
            .order_by(MediaItem.updated_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_statistics(self, db: AsyncSession, *, owner_id: int) -> dict:
        result = await db.execute(
            select(
                func.count(MediaItem.id).label('total'),
                func.count(case((MediaItem.status == "completed", 1))).label('completed'),
                func.count(case((MediaItem.status == "reading", 1))).label('reading'),
                func.count(case((MediaItem.status == "want_to_read", 1))).label('want_to_read'),
                func.count(case((MediaItem.media_type == "book", 1))).label('books'),
                func.count(case((MediaItem.media_type == "movie", 1))).label('movies'),
                func.count(case((MediaItem.media_type == "tv", 1))).label('tv_shows'),
                func.count(case((MediaItem.media_type == "podcast", 1))).label('podcasts')
            ).where(MediaItem.owner_id == owner_id)
        )
        stats = result.fetchone()
        return {
            "total": stats.total,
            "completed": stats.completed,
            "reading": stats.reading,
            "want_to_read": stats.want_to_read,
            "books": stats.books,
            "movies": stats.movies,
            "tv_shows": stats.tv_shows,
            "podcasts": stats.podcasts
        }


class MediaCollectionCRUD:
    async def get_by_id(self, db: AsyncSession, *, id: int) -> Optional[MediaCollection]:
        result = await db.execute(select(MediaCollection).where(MediaCollection.id == id))
        return result.scalar_one_or_none()
    
    async def get_multi(self, db: AsyncSession, *, owner_id: int) -> List[MediaCollection]:
        result = await db.execute(
            select(MediaCollection)
            .where(MediaCollection.owner_id == owner_id)
            .order_by(MediaCollection.is_default.desc(), MediaCollection.name.asc())
        )
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, *, obj_in: MediaCollectionCreate, owner_id: int) -> MediaCollection:
        db_obj = MediaCollection(**obj_in.dict(), owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, *, db_obj: MediaCollection, obj_in: MediaCollectionUpdate) -> MediaCollection:
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, *, id: int, owner_id: int) -> bool:
        collection = await self.get_by_id(db, id=id)
        if collection and collection.owner_id == owner_id:
            await db.delete(collection)
            await db.commit()
            return True
        return False
    
    async def get_default(self, db: AsyncSession, *, owner_id: int) -> Optional[MediaCollection]:
        result = await db.execute(
            select(MediaCollection)
            .where(and_(MediaCollection.owner_id == owner_id, MediaCollection.is_default == True))
        )
        return result.scalar_one_or_none()


media_item_crud = MediaItemCRUD()
media_collection_crud = MediaCollectionCRUD()