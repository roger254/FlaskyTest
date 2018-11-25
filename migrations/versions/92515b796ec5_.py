"""empty message

Revision ID: 92515b796ec5
Revises: 4d3b2baaaae9
Create Date: 2018-11-22 17:24:54.595374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92515b796ec5'
down_revision = '4d3b2baaaae9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
