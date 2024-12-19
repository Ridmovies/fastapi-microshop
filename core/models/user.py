from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.database import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
