from fastapi import status, Depends, APIRouter, Body, HTTPException
from .. import schemas, utils, oauth2
from ..database import cursor, conn
from ..schemas import Roles
from pydantic import parse_obj_as

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/{quiz_id}", response_model=schemas.QuestionOut)
def add_question(
    quiz_id: int,
    question: schemas.QuestionIn,
    admin_user=Depends(oauth2.get_admin_user),
):

    if question.author_id is None:
        question.author_id = admin_user.id

    print(question.possible_answers)

    cursor.execute(
        """        
        INSERT INTO questions (author_id, 
            points, 
            task_question, 
            task_description, 
            question_type, 
            possible_answers, 
            correct_answer) 
        VALUES (%s, %s, %s, %s, %s, %s, %s) 
        RETURNING *;            
        """,
        (
            question.author_id,
            question.points,
            question.task_question,
            question.task_description,
            question.question_type,
            question.possible_answers,
            question.correct_answer,
        ),
    )
    conn.commit()

    question_in_db = schemas.QuestionInDB(**cursor.fetchone())

    cursor.execute(
        """
        INSERT INTO quizes_questions
            (quiz_id, question_id)
        VALUES
            (%s, %s);           
        """,
        (
            quiz_id,
            question_in_db.id,
        ),
    )

    conn.commit()

    return question_in_db


@router.delete("/{question_id}")
def delete_question(
    quiz_id: int,
    admin_user=Depends(oauth2.get_admin_user),
):
    cursor.execute(
        """
        DELETE FROM questions WHERE id = %s;
        """,
        (quiz_id,),
    )
    conn.commit()

    return


@router.patch("/{question_id}", response_model=schemas.QuestionOut)
def edit_question(
    question_id: int,
    question: schemas.QuestionUpdate,
    admin_user=Depends(oauth2.get_admin_user),
):
    cursor.execute(
        """
        SELECT * FROM questions WHERE id = %s;
        """,
        (question_id,),
    )

    question_old = schemas.QuestionInDB(**cursor.fetchone())

    update_data = question.dict(exclude_unset=True)

    course_new = question_old.copy(update=update_data)

    cursor.execute(
        """
            UPDATE questions 
            SET author_id = %s, 
                points = %s, 
                task_question = %s,
                task_description = %s,
                question_type = %s,
                possible_answers = %s,
                correct_answer = %s
            WHERE id = %s 
            RETURNING *;
        """,
        (
            course_new.author_id,
            course_new.points,
            course_new.task_question,
            course_new.task_description,
            course_new.question_type,
            course_new.possible_answers,
            course_new.correct_answer,
            question_id,
        ),
    )

    returned = cursor.fetchone()
    conn.commit()

    return returned


@router.get("/{quiz_id}", response_model=list[schemas.QuestionOut])
def get_question_for_quiz(
    quiz_id: int,
    admin_user=Depends(oauth2.get_admin_user),
):
    cursor.execute(
        """
            SELECT * FROM questions 
            JOIN quizes_questions ON questions.id = quizes_questions.question_id
            WHERE quizes_questions.quiz_id = %s
        """,
        (quiz_id,),
    )

    questions = cursor.fetchall()

    conn.commit()

    return questions
