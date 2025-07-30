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
    return {"message": "Welcome to my API!!"}

# Function for getting posts


@app.get("/posts")
def get_posts():
    return {"data": "Here is your post"}


@app.post("/retrieve")
# Extract data sent in the body
def create_user(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"{payload['title']} content: {payload['content']}"}
