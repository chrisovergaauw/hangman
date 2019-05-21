"""empty message

Revision ID: 982512abcc22
Revises: ac8294c4a1d3
Create Date: 2019-05-21 17:00:51.598056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '982512abcc22'
down_revision = 'ac8294c4a1d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hangman', sa.Column('ts_created', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_hangman_ts_created'), 'hangman', ['ts_created'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_hangman_ts_created'), table_name='hangman')
    op.drop_column('hangman', 'ts_created')
    # ### end Alembic commands ###
