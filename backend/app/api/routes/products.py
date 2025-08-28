import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

from app.api.deps import SessionDep, get_current_active_superuser
from app.models import (
    Category,
    Message,
    Product,
    ProductCreate,
    ProductPublic,
    ProductsPublic,
    ProductUpdate,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=ProductsPublic)
def read_products(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """Retrieve products."""

    count_statement = select(func.count()).select_from(Product)
    count = session.exec(count_statement).one()
    statement = select(Product).offset(skip).limit(limit)
    products = session.exec(statement).all()
    return ProductsPublic(data=products, count=count)


@router.get("/{product_id}", response_model=ProductPublic)
def read_product(product_id: uuid.UUID, session: SessionDep) -> Any:
    """Get product by ID."""

    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ProductPublic,
)
def create_product(*, session: SessionDep, product_in: ProductCreate) -> Any:
    """Create new product."""

    category = session.get(Category, product_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    product = Product.model_validate(product_in)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.put(
    "/{product_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ProductPublic,
)
def update_product(
    *, session: SessionDep, product_id: uuid.UUID, product_in: ProductUpdate
) -> Any:
    """Update a product."""

    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product_in.category_id:
        category = session.get(Category, product_in.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    update_data = product_in.model_dump(exclude_unset=True)
    product.sqlmodel_update(update_data)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.delete("/{product_id}", dependencies=[Depends(get_current_active_superuser)])
def delete_product(session: SessionDep, product_id: uuid.UUID) -> Message:
    """Delete a product."""

    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return Message(message="Product deleted successfully")
