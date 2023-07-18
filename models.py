from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Numeric

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    current_salary = Column(Numeric)
    date_of_next_increase = Column(DateTime)
