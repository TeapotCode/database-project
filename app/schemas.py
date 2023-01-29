from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal
from enum import Enum

from pydantic.types import conint


class Roles(str, Enum):
    Student = "Student"
    Administrator = "Administrator"
    Moderator = "Moderator"
    Tutor = "Tutor"


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Roles


class UserDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Roles
    password: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    role: Roles
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class CourseOut(BaseModel):
    id: int
    name: str
    author_id: int


class CourseUpdate(BaseModel):
    name: str | None
    author_id: int | None
    password: str | None


class CourseCreate(BaseModel):
    name: str
    author_id: int | None
    password: str | None


class AccountCourseLink(BaseModel):
    id: int
    account_id: int
    course_id: int


class AccountCourseCreate(BaseModel):
    account_id: int
    course_id: int
