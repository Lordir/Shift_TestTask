import datetime
import decimal
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    current_salary: decimal.Decimal
    date_of_next_increase: datetime.datetime


class UserCreate(schemas.BaseUserCreate):
    current_salary: decimal.Decimal
    date_of_next_increase: datetime.datetime
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
