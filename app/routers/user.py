from fastapi import status, Depends, APIRouter, Body
from .. import schemas, utils, oauth2
from ..database import cursor, conn

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    cursor.execute(
        """
            INSERT INTO accounts (username, email, password, role) VALUES (%s, %s, %s, %s) RETURNING *
        """,
        (user.username, user.email, user.password, user.role),
    )
    new_user = cursor.fetchone()

    conn.commit()

    return new_user


@router.put(
    "/username", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut
)
def update_user(
    username: str = Body(), current_user: int = Depends(oauth2.get_current_user)
):

    cursor.execute(
        """
            UPDATE accounts
            SET username = %s
            WHERE id = %s
            RETURNING *
        """,
        (username, current_user.id),
    )

    conn.commit()
    user = cursor.fetchone()

    return user


@router.put(
    "/email", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut
)
def update_user(
    email: str = Body(),
    current_user: int = Depends(oauth2.get_current_user),
):

    cursor.execute(
        """
            UPDATE accounts
            SET email = %s
            WHERE id = %s
            RETURNING *
        """,
        (email, current_user.id),
    )
    conn.commit()

    user = cursor.fetchone()

    return user


@router.put(
    "/password", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut
)
def update_user(
    password: str = Body(), current_user: int = Depends(oauth2.get_current_user)
):

    hashed_password = utils.hash(password)

    cursor.execute(
        """
            UPDATE accounts
            SET password = %s
            WHERE id = %s
            RETURNING *
        """,
        (hashed_password, current_user.id),
    )
    conn.commit()

    user = cursor.fetchone()

    return user
