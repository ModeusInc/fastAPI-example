from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional
from typing import Annotated
from pydantic import Field

# -----------------------------
# Base schemas for Posts
# -----------------------------


class PostBase(BaseModel):
    """
    Shared properties for Post objects.
    - This base class ensures DRY: fields are reused across
      creation, updates, and responses.
    """
    title: str
    content: str
    published: bool = True  # Defaults to published unless explicitly set


class PostCreate(PostBase):
    """
    Schema for creating a Post.
    - Inherits all fields from PostBase.
    - Additional creation-only fields could be added later.
    """
    pass


# -----------------------------
# User schemas
# -----------------------------

class UserOut(BaseModel):
    """
    Public representation of a User.
    - Excludes sensitive information (like password hashes).
    - Used in responses (e.g., when returning the Post owner).
    """
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True  # Allow conversion from SQLAlchemy models


# Post response schema

class PostResponse(PostBase):
    """
    Schema for returning a Post in API responses.
    - Extends PostBase with DB-generated fields.
    - Includes a nested owner (UserOut) object for richer responses.
    """
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut  # Nested user schema (joined via relationship)

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    # this imply puts the fields from postresponse into this one field
    post: PostResponse
    votes: int

    class Config:
        orm_mode = True


# Authentication schemas

class UserCreate(BaseModel):
    """
    Schema for creating a new user (signup).
    - Includes only data the client is allowed to send.
    """
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Schema for logging in a user.
    - Same fields as UserCreate, but used specifically for authentication.
    """
    email: EmailStr
    password: str


class Token(BaseModel):
    """
    Schema representing a JWT access token.
    - Returned upon successful login/authentication.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for data extracted from a validated JWT.
    - Optional `id` allows distinguishing between invalid/missing tokens.
    """
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]
