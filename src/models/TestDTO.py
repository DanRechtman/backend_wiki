from typing import List,Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship



class Base(DeclarativeBase):
    pass
class Test(Base):
    __tablename__="test_col"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    IP: Mapped[str] = mapped_column(String(30),nullable=True)
    