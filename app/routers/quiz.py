from fastapi import status, Depends, APIRouter, Body, HTTPException
from .. import schemas, utils, oauth2
from ..database import cursor, conn
from ..schemas import Roles

router = APIRouter(prefix="/quizes", tags=["Quizes"])


@router.get("/all", response_model=list[schemas.QuizOut])
def get_all_quizes(user=Depends(oauth2.get_current_user)):
    cursor.execute(
        """
        SELECT * FROM quizes;
        """
    )
    return cursor.fetchall()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.QuizOut,
)
def add_quiz(
    quiz: schemas.QuizCreate,
    admin_user: schemas.UserCreate = Depends(oauth2.get_admin_user),
):

    cursor.execute(
        """
        INSERT INTO quizes (name,
            author_id, category, course_id, 
            difficulty, description, 
            password, time_open, time_close, attempts, time_to_complete)
        VALUES (%s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s)
        RETURNING *;
        """,
        (
            quiz.name,
            admin_user.id,
            quiz.category,
            quiz.course_id,
            quiz.difficulty,
            quiz.description,
            quiz.password,
            quiz.time_open,
            quiz.time_close,
            quiz.attempts,
            quiz.time_to_complete,
        ),
    )

    quiz = cursor.fetchone()

    conn.commit()

    return quiz


@router.delete(
    "/{quiz_id}",
    status_code=status.HTTP_200_OK,
)
def remove_quiz(
    quiz_id: int,
    admin_user: schemas.UserCreate = Depends(oauth2.get_admin_user),
):

    cursor.execute(
        """
        DELETE FROM quizes WHERE id = %s;
        """,
        (quiz_id,),
    )
    conn.commit()
    return {"details": f"Successfuly removed quiz id = {quiz_id}"}


@router.patch("/{quiz_id}", response_model=schemas.QuizOut)
def edit_quiz(
    quiz_id: int,
    quiz: schemas.QuizUpdate,
    admin_user: schemas.UserCreate = Depends(oauth2.get_admin_user),
):
    cursor.execute(
        """
            SELECT * FROM quizes WHERE id = %s;
        """,
        (quiz_id,),
    )

    quiz_old = schemas.QuizUpdate(**cursor.fetchone())

    update_data = quiz.dict(exclude_unset=True)

    quiz_new = quiz_old.copy(update=update_data)

    cursor.execute(
        """
            UPDATE quizes 
            SET name = %s, 
                author_id = %s, 
                course_id = %s, 
                category = %s,
                difficulty = %s,
                description = %s,
                password = %s,
                time_open = %s,
                time_close = %s,
                attempts = %s,
                time_to_complete = %s
            WHERE id = %s 
            RETURNING *;
        """,
        (
            quiz_new.name,
            quiz_new.author_id,
            quiz_new.course_id,
            quiz_new.category,
            quiz_new.difficulty,
            quiz_new.description,
            quiz_new.password,
            quiz_new.time_open,
            quiz_new.time_close,
            quiz_new.attempts,
            quiz.time_to_complete,
            quiz_id,
        ),
    )

    quiz_db = cursor.fetchone()
    conn.commit()

    return quiz_db
