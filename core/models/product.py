from sqlalchemy.orm import Mapped

from core.models.database import Base


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
