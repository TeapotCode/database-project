from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional, Literal
from enum import Enum

from pydantic.types import conint


class Roles(str, Enum):
    Student = "Student"
    Administrator = "Administrator"
    Moderator = "Moderator"
    Tutor = "Tutor"


class Difficulties(str, Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"
    Very_Hard = "Very Hard"
    Challenging = "Challenging"


class Categories(str, Enum):
    Math = "Math"
    Informatics = "Informatics"
    Physics = "Physics"
    Biology = "Biology"
    Chemistry = "Chemistry"
    History = "History"


class Grades(int, Enum):
    not_finished = 0
    F = 1
    F_plus = 1.5
    D = 2
    D_plus = 2.5
    C = 3
    C_plus = 3.5
    B = 4
    B_plus = 4.5
    A = 5
    A_plus = 5.5


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


class QuizBase(BaseModel):
    name: str
    author_id: int | None = None
    course_id: int
    category: Categories
    difficulty: Difficulties
    description: str
    attempts: int | None = 1
    time_open: datetime
    time_close: datetime
    time_to_complete: timedelta | None


class QuizCreate(QuizBase):
    password: str | None = None


class QuizOut(QuizBase):
    id: int


class QuizUpdate(BaseModel):
    name: Optional[str] = None
    author_id: Optional[int] = None
    course_id: Optional[int] = None
    category: Optional[Categories] = None
    difficulty: Optional[Difficulties] = None
    description: Optional[str] = None
    password: Optional[str] = None
    attempts: Optional[int] = None
    time_open: Optional[datetime] = None
    time_close: Optional[datetime] = None
    time_to_complete: Optional[timedelta] = None


class QuestionTypes(str, Enum):
    single = "Single choice"
    multiple = "Multiple choice"
    open = "Open"


class QuestionBase(BaseModel):
    author_id: int | None
    points: int = 1
    task_question: str
    task_description: str
    question_type: QuestionTypes
    possible_answers: list[str]

    class Config:
        orm_mode = True


class QuestionIn(QuestionBase):
    correct_answer: list[str]


class QuestionOut(QuestionBase):
    id: int


class QuestionInDB(QuestionBase):
    id: int
    correct_answer: list[str]


class QuestionUpdate(BaseModel):
    author_id: int = None
    points: int = None
    task_question: str = None
    task_description: str = None
    question_type: QuestionTypes = None
    possible_answers: list[str] = None
    correct_answer: list[str] = None
