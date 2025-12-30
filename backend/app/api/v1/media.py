from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from api.deps import get_current_active_user
from core.database import get_db
from crud.media import media_item_crud, media_collection_crud
from schemas.media import MediaItem, MediaItemCreate, MediaItemUpdate, MediaCollection, MediaCollectionCreate, MediaCollectionUpdate

router = APIRouter()


@router.get("/media", response_model=List[MediaItem])
async def get_media_items(
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    media_type: str = Query(None),
    status: str = Query(None),
    category: str = Query(None),
    tags: str = Query(None),
    search: str = Query(None)
) -> Any:
    items = await media_item_crud.get_multi(
        db,
        owner_id=current_user.id,
        skip=skip,
        limit=limit,
        media_type=media_type,
        status=status,
        category=category,
        tags=tags,
        search=search
    )
    return items


@router.post("/media", response_model=MediaItem)
async def create_media_item(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    media_in: MediaItemCreate
) -> Any:
    item = await media_item_crud.create(db, obj_in=media_in, owner_id=current_user.id)
    return item


@router.get("/media/{item_id}", response_model=MediaItem)
async def get_media_item(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    item_id: int
) -> Any:
    item = await media_item_crud.get_by_id(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return item


@router.put("/media/{item_id}", response_model=MediaItem)
async def update_media_item(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    item_id: int,
    media_in: MediaItemUpdate
) -> Any:
    item = await media_item_crud.get_by_id(db, id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Media item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    item = await media_item_crud.update(db, db_obj=item, obj_in=media_in)
    return item


@router.delete("/media/{item_id}")
async def delete_media_item(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    item_id: int
) -> Any:
    success = await media_item_crud.delete(db, id=item_id, owner_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Media item not found")
    return {"message": "Media item deleted successfully"}


@router.get("/media/status/{status}", response_model=List[MediaItem])
async def get_media_by_status(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    status: str
) -> Any:
    items = await media_item_crud.get_by_status(db, owner_id=current_user.id, status=status)
    return items


@router.get("/media/type/{media_type}", response_model=List[MediaItem])
async def get_media_by_type(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    media_type: str
) -> Any:
    items = await media_item_crud.get_by_type(db, owner_id=current_user.id, media_type=media_type)
    return items


@router.get("/media/recent", response_model=List[MediaItem])
async def get_recent_media(
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    limit: int = Query(10, ge=1, le=100)
) -> Any:
    items = await media_item_crud.get_recent(db, owner_id=current_user.id, limit=limit)
    return items


@router.get("/media/statistics")
async def get_media_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    stats = await media_item_crud.get_statistics(db, owner_id=current_user.id)
    return stats


@router.get("/collections", response_model=List[MediaCollection])
async def get_media_collections(
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    collections = await media_collection_crud.get_multi(db, owner_id=current_user.id)
    return collections


@router.post("/collections", response_model=MediaCollection)
async def create_media_collection(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    collection_in: MediaCollectionCreate
) -> Any:
    collection = await media_collection_crud.create(db, obj_in=collection_in, owner_id=current_user.id)
    return collection


@router.put("/collections/{collection_id}", response_model=MediaCollection)
async def update_media_collection(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    collection_id: int,
    collection_in: MediaCollectionUpdate
) -> Any:
    collection = await media_collection_crud.get_by_id(db, id=collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Media collection not found")
    if collection.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    collection = await media_collection_crud.update(db, db_obj=collection, obj_in=collection_in)
    return collection


@router.delete("/collections/{collection_id}")
async def delete_media_collection(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    collection_id: int
) -> Any:
    success = await media_collection_crud.delete(db, id=collection_id, owner_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Media collection not found")
    return {"message": "Media collection deleted successfully"}


@router.get("/collections/default", response_model=MediaCollection)
async def get_default_media_collection(
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    collection = await media_collection_crud.get_default(db, owner_id=current_user.id)
    if not collection:
        raise HTTPException(status_code=404, detail="Default media collection not found")
    return collection