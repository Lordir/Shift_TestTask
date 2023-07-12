from datetime import datetime, timedelta
from typing import Annotated, Union

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend
from fastapi_users.authentication import CookieTransport
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from fastapi import FastAPI, Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel

from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

cookie_transport = CookieTransport(cookie_max_age=600)
SECRET = "223157d3437024c37dadbcb4720cd672a581fb76ff59dfbfea835cfa5bc471fd"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

app = FastAPI()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 10


# fake_users_db = {
#     "testuser": {
#         "username": "testuser",
#         "hashed_password": '$2b$12$WWz2pGP8eMEFcwM8CRnBTOfydhd0JCPcHx67Imc1qyPZCC6IxkGb2',
#         "current_salary": 30000,
#         "date_of_next_increase": 10,
#     }
# }
