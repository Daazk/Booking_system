"""seed rooms

Revision ID: 55d3342e1ea9
Revises: 9c2d99686b6e
Create Date: 2026-10-04 07:36:22.532584

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "55d3342e1ea9"
down_revision: Union[str, Sequence[str], None] = "9c2d99686b6e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    rooms_table = sa.table(
        "rooms",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("capacity", sa.Integer),
    )
    op.bulk_insert(
        rooms_table,
        [
            {"name": "room #1", "capacity": 3},
            {"name": "room #2", "capacity": 2},
            {"name": "room #3", "capacity": 7},
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM rooms WHERE name IN ('room #1', 'room #2', 'room #3')")
