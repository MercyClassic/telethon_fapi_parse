from typing import TYPE_CHECKING

from db.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from db.models import User


class Message(Base):
    __tablename__ = 'message'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    from_phone: Mapped[str] = mapped_column(ForeignKey('account.phone_number'))
    message_text: Mapped[str]

    user: Mapped['User'] = relationship(back_populates='messages')
