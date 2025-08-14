from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

# Instance name
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
def root():
    return {"message": "Welcome to my world!! Curious to see where this goes!!!"}

# Function for getting posts


@app.get("/posts")
def get_posts():
    return {"data": "Here is your post"}


@app.post("/retrieve")
# Extract data sent in the body
def create_user(new_post: Post):
    print(new_post)
    return {"data": "new post"}
