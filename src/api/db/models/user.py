from typing import TYPE_CHECKING, List

from db.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models import Message


class User(Base):
    __tablename__ = 'account'

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(unique=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    tokens: Mapped[List['Token']] = relationship(back_populates='user')
    messages: Mapped[List['Message']] = relationship(back_populates='user')


class Token(Base):
    __tablename__ = 'token'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('account.id'))
    token: Mapped[str]

    user: Mapped['User'] = relationship(back_populates='tokens')
