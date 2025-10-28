import random

from sqlmodel import Session

from app.models import Product, ProductCreate
from app.tests.utils.category import create_random_category
from app.tests.utils.utils import random_lower_string


def create_random_product(db: Session) -> Product:
    category = create_random_category(db)
    category_id = category.id
    name = random_lower_string()
    description = random_lower_string()
    price = random.uniform(10, 100)
    product_in = ProductCreate(
        name=name, description=description, price=price, category_id=category_id
    )
    db_obj = Product.model_validate(product_in)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
