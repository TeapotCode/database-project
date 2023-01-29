"""add difficulties

Revision ID: ba3e188b2c5f
Revises: a48101f4cbe7
Create Date: 2023-01-20 00:58:17.281728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ba3e188b2c5f"
down_revision = "a48101f4cbe7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        """
        CREATE TABLE difficulties (
            id integer GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            name varchar(255) NOT NULL UNIQUE
        );
        
        
        INSERT INTO difficulties (name) 
        VALUES ('Easy'), ('Medium'), ('Hard'), ('Very Hard'), ('Challenging');
        """
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        """
        DROP TABLE difficulties;
        """
    )
