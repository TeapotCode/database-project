"""add view accounts assigned to course

Revision ID: 3f86576dc722
Revises: 12358653f73b
Create Date: 2023-01-29 13:28:20.262272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3f86576dc722"
down_revision = "12358653f73b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        """
        CREATE VIEW view_accounts_assigned_to_course AS
        SELECT courses.id as course_id, 
                courses.name as course_name, 
                courses.author_id as author_id,
                accounts_courses.account_id as assigned_account_id
        FROM courses 
        JOIN accounts_courses ON courses.id = accounts_courses.course_id;
        """
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        """
        DROP VIEW IF EXISTS view_accounts_assigned_to_course;
        """
    )
