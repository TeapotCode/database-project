"""add category

Revision ID: a48101f4cbe7
Revises: f9c8a032910d
Create Date: 2023-01-20 00:57:01.141749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a48101f4cbe7"
down_revision = "f9c8a032910d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        """
        CREATE TABLE categories (
            id integer GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            name varchar(255) NOT NULL
        );
        
        
        INSERT INTO categories (name) 
        VALUES ('Math'), ('Informatics'), ('Physics'), ('Biology'), ('Chemistry'), ('History'); 
        """
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        """
        DROP TABLE categories;
        """
    )