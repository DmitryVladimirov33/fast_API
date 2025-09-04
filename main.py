from fastapi import FastAPI, HTTPException
import uvicorn
import secrets
from pydantic import BaseModel


app = FastAPI()


def generate_hex(elem, **kwargs):
    return secrets.token_hex(int(elem) // 2)


users = [
    {
        "id": 1,
        "uuid": generate_hex(16),
        "name": "Иван",
        "surname": "Иванов",
        "age": 25
    },
    {
        "id": 2,
        "uuid": generate_hex(16),
        "name": "Сергей",
        "surname": "Петров",
        "age": 30
    }
]


@app.get("/users", summary="Получение пользователей", tags=["Основные методы"])
def get_all_users():
    return users


@app.get("/users/{uuid}", summary="Получение пользователя по uuid", tags=["Основные методы"])
def get_users(uuid: str):
    for user in users:
        if user["uuid"] == uuid:
            return user

    raise HTTPException(status_code=404, detail="Пользователь не существует")


class NewUser(BaseModel):
    name: str
    surname: str
    age: int


@app.post("/users", summary="Добавление пользователя", tags=["Основные методы"])
def post_all_users(new_user: NewUser):
    users.append({
        "id": len(users) + 1,
        "uuid": generate_hex(16),
        "name": new_user.name,
        "surname": new_user.surname,
        "age": new_user.age
     })
    return new_user


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
