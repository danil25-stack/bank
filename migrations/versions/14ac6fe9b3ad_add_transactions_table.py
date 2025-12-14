"""add transactions table

Revision ID: 14ac6fe9b3ad
Revises: 600616dbf623
Create Date: 2025-12-10 11:53:34.623268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14ac6fe9b3ad'
down_revision: Union[str, Sequence[str], None] = '600616dbf623'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- create enum type FIRST ---
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'source_type_enum') THEN
            CREATE TYPE source_type_enum AS ENUM (
                'ATM',
                'BANK_TRANSFER',
                'POS',
                'SALARY',
                'COMMERCE_PAYMENTS'
            );
        END IF;
    END$$;
    """)

    # --- your existing operations ---
    op.drop_constraint(op.f('account_psu_id_fkey'),
                       'account', type_='foreignkey')
    op.create_foreign_key(None, 'account', 'psu', ['psu_id'], [
                          'id'], ondelete='CASCADE')

    op.alter_column(
        'psu', 'psu_number',
        existing_type=sa.VARCHAR(),
        nullable=False
    )

    # --- add enum column ---
    op.add_column(
        'transaction',
        sa.Column(
            'source_type',
            sa.Enum(
                'ATM',
                'BANK_TRANSFER',
                'POS',
                'SALARY',
                'COMMERCE_PAYMENTS',
                name='source_type_enum'
            ),
            nullable=False
        )
    )


def downgrade() -> None:
    op.drop_column('transaction', 'source_type')

    op.alter_column(
        'psu', 'psu_number',
        existing_type=sa.VARCHAR(),
        nullable=True
    )

    op.drop_constraint(None, 'account', type_='foreignkey')
    op.create_foreign_key(
        op.f('account_psu_id_fkey'),
        'account',
        'psu',
        ['psu_id'],
        ['id']
    )

    # --- drop enum type ---
    op.execute("DROP TYPE IF EXISTS source_type_enum")
