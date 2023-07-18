from typing import Annotated, Union
from datetime import date, timedelta
from databases import Database

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.responses import Response

from additional import verify_password, get_password_hash, create_access_token, OAuth2PasswordBearerWithCookie
from models import User

SECRET_KEY = '331da708546f45de48c5a370a1daa0bde99013885982db25420ae25b7ae737b9'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
DATABASE_URL = "sqlite+aiosqlite:///test.db"

database = Database(DATABASE_URL)


async def create_test_user():
    query = "INSERT INTO User(username, hashed_password, current_salary, date_of_next_increase) VALUES (:username, " \
            ":hashed_password, :current_salary, :date_of_next_increase)"
    values = [{"username": "testuser", "hashed_password": get_password_hash("password"), "current_salary": 30000,
               "date_of_next_increase": date(2023, 8, 15)}]

    result = await database.execute_many(query=query, values=values)
    return result


# asyncio.run(create_test_user())


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    query = f"SELECT * FROM User WHERE username='{token_data.username}'"
    user = await database.fetch_one(query=query)

    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@app.post("/token")
async def login(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    query = f"SELECT * FROM User WHERE username='{form_data.username}'"
    user = await database.fetch_one(query=query)

    if not verify_password(form_data.password, user["hashed_password"]):
        return {'Результат': 'Неверный пароль'}
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {'Результат': 'Вы успешно авторизованы'}


@app.get("/get_data")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return {'Текущая зарплата': current_user.current_salary,
            'Дата следующего повышения': current_user.date_of_next_increase}
