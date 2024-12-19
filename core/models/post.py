from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.database import Base


class Post(Base):
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text, default="", server_default="")

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User", back_populates="posts")