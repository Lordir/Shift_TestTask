from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin

from auth.database import User, get_user_db

SECRET = "SECRET_KEY"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
