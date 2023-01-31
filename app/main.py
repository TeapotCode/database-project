from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import quiz, user, auth, course, question


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(course.router)
app.include_router(quiz.router)
app.include_router(question.router)
