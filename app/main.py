import uvicorn
from fastapi import FastAPI

from app.db.base import Base, engine
from app.routers.task_router import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix = "/tasks")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager!"}

if __name__ == "__main__":
    uvicorn.run("task_manager:app", host="127.0.0.1", port=8001, reload=False)