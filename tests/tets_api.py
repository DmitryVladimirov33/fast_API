import pytest
from httpx import AsyncClient, ASGITransport

from main import app, generate_hex, users, get_all_users


@pytest.mark.asyncio
async def test_get_all_users():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as async_client:
        response = await async_client.get("/users")
        assert response.status_code == 200
        data = response.json()
        assert data != []


@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as async_client:
        uuid = get_all_users()[0]["uuid"]
        name = get_all_users()[0]["name"]
        surname = get_all_users()[0]["surname"]
        age = get_all_users()[0]["age"]

        response = await async_client.get(f"/users/{uuid}")

        assert response.status_code == 200

        data = response.json()

        assert data["id"] is not None
        assert data["uuid"] == uuid
        assert data["name"] == name
        assert data["surname"] == surname
        assert data["age"] == age


@pytest.mark.asyncio
async def test_post_get_users_valid_values():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as async_client:
        response = await async_client.post("/users", json={
            "id": len(users) + 1,
            "uuid": generate_hex(16),
            "name": "Иван",
            "surname": "Иванов",
            "age": 22
        })
        assert response.status_code == 200
        data = response.json()
        assert data == {'age': 22, 'name': 'Иван', 'surname': 'Иванов'}


@pytest.mark.parametrize('name, surname, age, value',
                         [(123, "Иванов", 22, {'detail': [{'input': 123,
                                                           'loc': ['body', 'name'],
                                                           'msg': 'Input should be a valid string',
                                                           'type': 'string_type'}]}),
                          ("Иван", 123, 22, {'detail': [{'input': 123,
                                                         'loc': ['body', 'surname'],
                                                         'msg': 'Input should be a valid string',
                                                         'type': 'string_type'}]}),
                          ("Иван", "Иванов", "двадцать", {'detail': [{'input': 'двадцать',
                                                                      'loc': ['body', 'age'],
                                                                      'msg': 'Input should be a valid integer, unable '
                                                                             'to parse string as an integer',
                                                                      'type': 'int_parsing'}]})])
@pytest.mark.asyncio
async def test_post_get_users_invalid_values(name, surname, age, value):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as async_client:
        response = await async_client.post("/users", json={
            "id": len(users) + 1,
            "uuid": generate_hex(16),
            "name": name,
            "surname": surname,
            "age": age,
        })
        assert response.status_code == 422
        data = response.json()
        assert data == value
