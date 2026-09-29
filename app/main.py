from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
def main():
    return {"message": "Hello, World!"}
