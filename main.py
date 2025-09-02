from fastapi import FastAPI
import uvicorn

app = FastAPI()

users = [
    {
        "id": 1,
        "name": "Иван",
        "surname": "Иванов",
        "age": 25
    },
    {
        "id": 2,
        "name": "Сергей",
        "surname": "Петров",
        "age": 30
    }
]


@app.get("/users")
def get_users():
    return users


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
