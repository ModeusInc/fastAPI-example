from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# Instance name
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://www.google.com",
    "http://localhost",
    "http://localhost:8000",
    "chrome-untrusted://*",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
# Responsible for creating the table if not originally there
# models.Base.metadata.create_all(bind=engine)

# connects routers to FastAPI instance
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
