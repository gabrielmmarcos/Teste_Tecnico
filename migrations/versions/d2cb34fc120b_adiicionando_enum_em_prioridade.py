"""adiicionando enum em prioridade

Revision ID: d2cb34fc120b
Revises: caf4832b9f5c
Create Date: 2026-05-28 13:41:12.021891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2cb34fc120b'
down_revision: Union[str, Sequence[str], None] = 'caf4832b9f5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


prioridade_enum = sa.Enum(
    'ALTA',
    'NORMAL',
    name='prioridadeenum'
)

def upgrade() -> None:
    """Upgrade schema."""

 
    prioridade_enum.create(op.get_bind(), checkfirst=True)

    op.execute("""
        ALTER TABLE clientes
        ALTER COLUMN prioridade
        TYPE prioridadeenum
        USING prioridade::prioridadeenum
    """)

    op.alter_column(
        'clientes',
        'prioridade',
        existing_type=sa.VARCHAR(),
        type_=sa.Enum(
            'ALTA',
            'NORMAL',
            name='prioridadeenum'
        ),
        existing_nullable=True
    )

def downgrade() -> None:
    """Downgrade schema."""

    op.execute("""  
        ALTER TABLE clientes
        ALTER COLUMN prioridade
        TYPE VARCHAR
        USING prioridade::text
    """)

    prioridade_enum.drop(op.get_bind(), checkfirst=True)