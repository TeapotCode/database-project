from fastapi import status, Depends, APIRouter, Body, HTTPException
from .. import schemas, utils, oauth2
from ..database import cursor, conn
from ..schemas import Roles

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=list[schemas.CourseOut])
def get_courses():
    cursor.execute(
        """
        SELECT * FROM courses
        """
    )

    courses = cursor.fetchall()
    return courses


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.CourseOut)
def create_course(
    course: schemas.CourseCreate, admin_user: int = Depends(oauth2.get_admin_user)
):

    if not course.author_id:
        course.author_id = admin_user.id

    cursor.execute(
        """
        INSERT INTO courses (name, author_id, password) VALUES (%s, %s, %s) RETURNING *
        """,
        (course.name, course.author_id, course.password),
    )

    new_course = cursor.fetchone()
    conn.commit()

    return new_course


@router.get("/owned/", response_model=list[schemas.CourseOut])
def get_my_courses(current_user=Depends(oauth2.get_current_user)):

    cursor.execute(
        """
        SELECT * FROM courses WHERE author_id = %s
        """,
        (current_user.id,),
    )

    courses = cursor.fetchall()
    return courses


@router.post(
    "/users/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AccountCourseLink,
)
def add_account_course(
    account_course: schemas.AccountCourseCreate,
    admin_user: schemas.UserCreate = Depends(oauth2.get_admin_user),
):
    cursor.execute(
        """
        INSERT INTO accounts_courses (account_id, course_id) VALUES (%s, %s) RETURNING *
        """,
        (account_course.account_id, account_course.course_id),
    )

    link = cursor.fetchone()
    conn.commit()

    return link


@router.post(
    "/join/{course_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AccountCourseLink,
)
def join_course(
    course_id: int,
    password: str | None = Body(None),
    current_user=Depends(oauth2.get_current_user),
):
    cursor.execute(
        """
            SELECT * FROM courses WHERE id = %s
        """,
        (course_id,),
    )
    selected_course = cursor.fetchone()
    if not selected_course:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid course id"
        )

    course_password = schemas.CourseCreate(**selected_course).password
    if password != course_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid course password"
        )

    cursor.execute(
        """
        INSERT INTO accounts_courses (account_id, course_id) VALUES (%s, %s) RETURNING *          
        """,
        (current_user.id, course_id),
    )

    link = cursor.fetchone()
    conn.commit()

    return link


@router.patch(
    "/{course_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.CourseOut,
)
def edit_course(
    course_id: int,
    course: schemas.CourseUpdate,
    admin_user: schemas.UserCreate = Depends(oauth2.get_admin_user),
):
    cursor.execute(
        """
                    SELECT * FROM courses WHERE id = %s;
                   """,
        (course_id,),
    )

    course_old = schemas.CourseUpdate(**cursor.fetchone())

    update_data = course.dict(exclude_unset=True)

    course_new = course_old.copy(update=update_data)

    cursor.execute(
        """
            UPDATE courses SET name = %s, author_id = %s, password = %s WHERE id = %s RETURNING *;
        """,
        (course_new.name, course_new.author_id, course_new.password, course_id),
    )

    link = cursor.fetchone()
    conn.commit()

    return link


@router.delete(
    "/{course_id}",
    response_model=schemas.CourseOut,
)
def remove_course(
    course_id: int,
    admin_user: schemas.UserCreate = Depends(oauth2.get_admin_user),
):

    cursor.execute(
        """
            DELETE FROM courses WHERE id = %s RETURNING *;
        """,
        (course_id,),
    )

    course = cursor.fetchone()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid course id = {course_id}",
        )

    conn.commit()

    return course


@router.post(
    "/leave/{course_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.AccountCourseLink,
)
def leave_course(
    course_id: int,
    password: str | None = Body(None),
    current_user=Depends(oauth2.get_current_user),
):
    cursor.execute(
        """
            SELECT * FROM courses WHERE id = %s
        """,
        (course_id,),
    )
    selected_course = cursor.fetchone()
    if not selected_course:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid course id"
        )

    course_password = schemas.CourseCreate(**selected_course).password
    if password != course_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid course password"
        )

    cursor.execute(
        """
        DELETE FROM accounts_courses WHERE account_id = %s AND course_id = %s RETURNING *          
        """,
        (current_user.id, course_id),
    )

    link = cursor.fetchone()
    conn.commit()

    if link is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"User was not in course"
        )

    return link


@router.delete(
    "/users/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.AccountCourseLink,
)
def remove_account_course(
    account_course: schemas.AccountCourseCreate,
    admin_user: schemas.UserCreate = Depends(oauth2.get_admin_user),
):
    cursor.execute(
        """
        DELETE FROM accounts_courses WHERE account_id = %s AND course_id = %s RETURNING *
        """,
        (
            account_course.account_id,
            account_course.course_id,
        ),
    )

    link = cursor.fetchone()
    conn.commit()

    if not link:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"User is not in course"
        )

    return link


@router.get(
    "/assigned/",
    status_code=status.HTTP_200_OK,
)
def assigned_courses(
    current_user=Depends(oauth2.get_current_user),
):
    cursor.execute(
        """
        SELECT * FROM view_accounts_assigned_to_course WHERE assigned_account_id = %s
        """,
        (current_user.id,),
    )

    course = cursor.fetchall()

    return course


# TODO
# statystyki kursu
# statystyki usera
# CRUD zadania + statystyki
