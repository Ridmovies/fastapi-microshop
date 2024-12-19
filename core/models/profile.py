from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models.database import Base
from core.models.mixins import UserRelationMixin


class Profile(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profile"

    firstname: Mapped[str | None] = mapped_column(String(32))
    lastname: Mapped[str | None] = mapped_column(String(32))
    bio: Mapped[str | None]

    # user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
