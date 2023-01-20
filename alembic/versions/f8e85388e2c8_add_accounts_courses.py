"""add accounts_courses

Revision ID: f8e85388e2c8
Revises: 3d78a59e2428
Create Date: 2023-01-20 01:22:50.518509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f8e85388e2c8"
down_revision = "3d78a59e2428"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        """
        CREATE TABLE accounts_courses (
            id integer GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            account_id integer REFERENCES accounts(id) NOT NULL,
            course_id integer REFERENCES courses(id) NOT NULL
        );
        """
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        """
        DROP TABLE accounts_courses;
        """
    )