from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


from app.db.base import Base, engine
from app.routers.task_router import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Allow CORS (Cross-Origin Resource Sharing) to enable JS from the frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix = "/tasks")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager!"}
