from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_active_user
from app.core.database import get_db
from app.crud.card import knowledge_card_crud, notebook_crud
from app.schemas.card import KnowledgeCard, KnowledgeCardCreate, KnowledgeCardUpdate, Notebook, NotebookCreate, NotebookUpdate

router = APIRouter()


@router.get("/cards", response_model=List[KnowledgeCard])
async def get_knowledge_cards(
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: str = Query(None),
    tags: str = Query(None),
    status: str = Query(None),
    search: str = Query(None)
) -> Any:
    cards = await knowledge_card_crud.get_multi(
        db,
        owner_id=current_user.id,
        skip=skip,
        limit=limit,
        category=category,
        tags=tags,
        status=status,
        search=search
    )
    return cards


@router.post("/cards", response_model=KnowledgeCard)
async def create_knowledge_card(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    card_in: KnowledgeCardCreate
) -> Any:
    card = await knowledge_card_crud.create(db, obj_in=card_in, owner_id=current_user.id)
    return card


@router.get("/cards/{card_id}", response_model=KnowledgeCard)
async def get_knowledge_card(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    card_id: int
) -> Any:
    card = await knowledge_card_crud.get_by_id(db, id=card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Knowledge card not found")
    if card.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return card


@router.put("/cards/{card_id}", response_model=KnowledgeCard)
async def update_knowledge_card(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    card_id: int,
    card_in: KnowledgeCardUpdate
) -> Any:
    card = await knowledge_card_crud.get_by_id(db, id=card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Knowledge card not found")
    if card.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    card = await knowledge_card_crud.update(db, db_obj=card, obj_in=card_in)
    return card


@router.delete("/cards/{card_id}")
async def delete_knowledge_card(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    card_id: int
) -> Any:
    success = await knowledge_card_crud.delete(db, id=card_id, owner_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Knowledge card not found")
    return {"message": "Knowledge card deleted successfully"}


@router.get("/cards/favorites", response_model=List[KnowledgeCard])
async def get_favorite_cards(
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
) -> Any:
    cards = await knowledge_card_crud.get_favorites(db, owner_id=current_user.id, skip=skip, limit=limit)
    return cards


@router.get("/cards/recent", response_model=List[KnowledgeCard])
async def get_recent_cards(
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    limit: int = Query(10, ge=1, le=100)
) -> Any:
    cards = await knowledge_card_crud.get_recent(db, owner_id=current_user.id, limit=limit)
    return cards


@router.get("/notebooks", response_model=List[Notebook])
async def get_notebooks(
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    notebooks = await notebook_crud.get_multi(db, owner_id=current_user.id)
    return notebooks


@router.post("/notebooks", response_model=Notebook)
async def create_notebook(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    notebook_in: NotebookCreate
) -> Any:
    notebook = await notebook_crud.create(db, obj_in=notebook_in, owner_id=current_user.id)
    return notebook


@router.put("/notebooks/{notebook_id}", response_model=Notebook)
async def update_notebook(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    notebook_id: int,
    notebook_in: NotebookUpdate
) -> Any:
    notebook = await notebook_crud.get_by_id(db, id=notebook_id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    if notebook.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    notebook = await notebook_crud.update(db, db_obj=notebook, obj_in=notebook_in)
    return notebook


@router.delete("/notebooks/{notebook_id}")
async def delete_notebook(
    *,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user),
    notebook_id: int
) -> Any:
    success = await notebook_crud.delete(db, id=notebook_id, owner_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return {"message": "Notebook deleted successfully"}


@router.get("/notebooks/default", response_model=Notebook)
async def get_default_notebook(
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_active_user)
) -> Any:
    notebook = await notebook_crud.get_default(db, owner_id=current_user.id)
    if not notebook:
        raise HTTPException(status_code=404, detail="Default notebook not found")
    return notebook