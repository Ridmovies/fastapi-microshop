from datetime import datetime

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    DateTime,
    func,
    Table,
    Column,
    Integer,
    UniqueConstraint,
    INTEGER,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from tomlkit.items import Integer

from core.models.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(32), unique=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")

    def __str__(self):
        return f"<User {self.username}>"


class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True)

    firstname: Mapped[str | None] = mapped_column(String(32))
    lastname: Mapped[str | None] = mapped_column(String(32))
    bio: Mapped[str | None]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="profile")

    def __repr__(self):
        return f"<Profile {self.firstname} {self.lastname}>"


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text, default="", server_default="")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")


order_product_association = Table(
    "order_product_association",
    Base.metadata,
    Column("id", INTEGER, primary_key=True),
    Column("order_id", ForeignKey("orders.id"), nullable=False),
    Column("product_id", ForeignKey("products.id"), nullable=False),
    UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
)


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    orders: Mapped[list["Order"]] = relationship(
        secondary=order_product_association, back_populates="products"
    )


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, server_default=func.now()
    )
    products: Mapped[list["Product"]] = relationship(
        secondary=order_product_association, back_populates="orders"
    )
