from sqlalchemy import Column, Integer, String, DateTime, Numeric, Boolean
from auth.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String)
    current_salary = Column(Numeric, index=True)
    date_of_next_increase = Column(DateTime, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)


