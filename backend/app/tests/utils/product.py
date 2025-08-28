from sqlmodel import Session

from app import crud
from app.models import Product, ProductCreate
from app.tests.utils.category import create_random_category
from app.tests.utils.utils import random_lower_string


def create_random_product(db: Session) -> Product:
    category = create_random_category(db)
    name = random_lower_string()
    description = random_lower_string()
    price = 1.0
    product_in = ProductCreate(
        name=name,
        description=description,
        price=price,
        category_id=category.id,
    )
    return crud.create_product(session=db, product_in=product_in)
