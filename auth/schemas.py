import datetime
import decimal

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    current_salary: decimal.Decimal
    date_of_next_increase: datetime.datetime


class UserCreate(schemas.BaseUserCreate):
    current_salary: decimal.Decimal
    date_of_next_increase: datetime.datetime
