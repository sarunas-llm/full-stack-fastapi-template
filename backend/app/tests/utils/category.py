from sqlmodel import Session

from app.models import Category, CategoryCreate
from app.tests.utils.utils import random_lower_string


def create_random_category(db: Session) -> Category:
    name = random_lower_string()
    description = random_lower_string()
    category_in = CategoryCreate(name=name, description=description)
    db_obj = Category.model_validate(category_in)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
