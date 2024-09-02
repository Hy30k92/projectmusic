from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from app.model.base import Base


class Member(Base):
    __tablename__ = 'member'

    mno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    userid: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    passwd: Mapped[str]
    name: Mapped[str]
    email: Mapped[str]
    regdate: Mapped[datetime] = mapped_column(default=datetime.now)


    class Pay(Base):
        __tablename__ = 'pay'

        pno: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
        userid: Mapped[str] = mapped_column(ForeignKey('member.userid'), index=True)
        passwd: Mapped[str]
        email: Mapped[str]
        regdate: Mapped[datetime] = mapped_column(default=datetime.now)
        eregdate: Mapped[datetime] = mapped_column(default=datetime.now)
