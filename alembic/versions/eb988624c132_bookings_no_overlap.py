"""bookings no overlap

Revision ID: eb988624c132
Revises: 55d3342e1ea9
Create Date: 2026-10-06 18:48:04.352197

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "eb988624c132"
down_revision: Union[str, Sequence[str], None] = "55d3342e1ea9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    op.execute("""
        ALTER TABLE bookings
        ADD CONSTRAINT bookings_no_overlap
        EXCLUDE USING gist (
            room_id WITH =,
            tstzrange(start_time, end_time, '[)') WITH &&
        )
    """)  # [) означает диапазон от start_time включительно до end_time не включительно
    # && значит пересикаються ли два диапазона


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE bookings DROP CONSTRAINT bookings_no_overlap")
    # выполниться если я откачу миграцию
