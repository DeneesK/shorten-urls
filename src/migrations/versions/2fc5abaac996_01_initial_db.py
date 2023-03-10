"""01_initial-db

Revision ID: 2fc5abaac996
Revises: 
Create Date: 2023-02-09 13:59:36.567739

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2fc5abaac996'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('original_url', sa.Text(), nullable=False, unique=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_url_created_at'), 'url', ['created_at'], unique=False)
    op.create_table('history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('url_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('counter', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['url_id'], ['url.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('history')
    op.drop_index(op.f('ix_url_created_at'), table_name='url')
    op.drop_table('url')
    # ### end Alembic commands ###
