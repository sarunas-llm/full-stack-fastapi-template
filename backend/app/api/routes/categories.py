import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep, get_current_active_superuser
from app.models import (
    CategoriesPublic,
    Category,
    CategoryCreate,
    CategoryPublic,
    CategoryUpdate,
    Message,
    Product,
)

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=CategoriesPublic)
def read_categories(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """Retrieve categories."""

    count_statement = select(func.count()).select_from(Category)
    count = session.exec(count_statement).one()
    statement = select(Category).offset(skip).limit(limit)
    categories = session.exec(statement).all()
    return CategoriesPublic(data=categories, count=count)


@router.get("/{category_id}", response_model=CategoryPublic)
def read_category(category_id: uuid.UUID, session: SessionDep) -> Any:
    """Get category by ID."""

    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=CategoryPublic,
)
def create_category(*, session: SessionDep, category_in: CategoryCreate) -> Any:
    """Create new category."""

    category = Category.model_validate(category_in)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.put(
    "/{category_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=CategoryPublic,
)
def update_category(
    *, session: SessionDep, category_id: uuid.UUID, category_in: CategoryUpdate
) -> Any:
    """Update a category."""

    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    update_data = category_in.model_dump(exclude_unset=True)
    category.sqlmodel_update(update_data)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete("/{category_id}", dependencies=[Depends(get_current_active_superuser)])
def delete_category(session: SessionDep, category_id: uuid.UUID) -> Message:
    """Delete a category without products."""

    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    count_products = session.exec(
        select(func.count())
        .select_from(Product)
        .where(Product.category_id == category_id)
    ).one()
    if count_products:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category with existing products",
        )
    session.delete(category)
    session.commit()
    return Message(message="Category deleted successfully")
