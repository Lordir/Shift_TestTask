from datetime import date

from httpx import AsyncClient

from additional import get_password_hash
from tests.conftest import database, client


async def test_create_testuser():
    query = "INSERT INTO User(username, hashed_password, current_salary, date_of_next_increase) VALUES (:username, " \
            ":hashed_password, :current_salary, :date_of_next_increase)"
    values = [{"username": "testuser", "hashed_password": get_password_hash("password"), "current_salary": 30000,
               "date_of_next_increase": date(2023, 8, 15)}]
    await database.execute_many(query=query, values=values)

    query = f"SELECT * FROM User WHERE username='testuser'"
    user = await database.fetch_one(query=query)

    assert user.username == "testuser", "Пользователь не добавлен"


def test_get_data_without_cookies():
    response = client.get("/get_data")

    assert response.status_code == 401


def test_login():
    response = client.post("/token", data={"username": "testuser", "password": "password"})

    assert response.status_code == 200


def test_login_token_in_cookies():
    response = client.post("/token", data={"username": "testuser", "password": "password"})

    assert response.cookies["access_token"]


def test_get_data():
    response = client.get("/get_data")
    data = response.json()

    assert response.status_code == 200
    assert data == {'Текущая зарплата': 30000, 'Дата следующего повышения': '2023-08-15'}


async def test_get_data_async_without_cookies(ac: AsyncClient):
    response = await ac.get("/get_data")

    assert response.status_code == 401


async def test_login_async(ac: AsyncClient):
    response = await ac.post("/token", data={"username": "testuser", "password": "password"})

    assert response.status_code == 200


async def test_get_data_async(ac: AsyncClient):
    response = await ac.get("/get_data")
    data = response.json()

    assert response.status_code == 200
    assert data == {'Текущая зарплата': 30000, 'Дата следующего повышения': '2023-08-15'}
