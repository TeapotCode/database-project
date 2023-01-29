from fastapi import status, Depends, APIRouter, Body, HTTPException
from .. import schemas, utils, oauth2
from ..database import cursor, conn
from ..schemas import Roles

router = APIRouter(prefix="/quizes", tags=["Quizes"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.QuizOut,
)
def add_quiz(
    quiz: schemas.QuizCreate,
    admin_user: schemas.UserCreate = Depends(oauth2.get_admin_user),
):

    print(
        quiz.name,
        admin_user.id,
        quiz.category,
        quiz.course_id,
        quiz.category,
        quiz.difficulty,
        quiz.description,
        quiz.password,
        # quiz.attempts,
        quiz.time_open,
        quiz.time_close,
        quiz.time_to_complete,
    )

    # cursor.execute(
    #     """
    #     INSERT INTO quizes (name,
    #         author_id, category, course_id,
    #         category, difficulty, description,
    #         password, time_open, time_close)
    #     VALUES name = %s,
    #         author_id = %s,
    #         category = %s,
    #         difficulty = %s,
    #         description = %s,
    #         password = %s,

    #         time_open = %s,
    #         time_close = %s,
    #     RETURNING *;
    #     """,
    #     (
    #         quiz.name,
    #         admin_user.id,
    #         quiz.category,
    #         quiz.course_id,
    #         quiz.category,
    #         quiz.difficulty,
    #         quiz.description,
    #         quiz.password,
    #         # quiz.attempts,
    #         quiz.time_open,
    #         quiz.time_close,
    #         quiz.time_to_complete,
    #     ),
    # )

    quiz = cursor.fetchone()

    conn.commit()

    return quiz
