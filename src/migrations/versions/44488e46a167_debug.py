"""debug

Revision ID: 44488e46a167
Revises: fd13637d4beb
Create Date: 2021-05-09 22:49:47.836797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44488e46a167'
down_revision = 'fd13637d4beb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('color', sa.String(length=7), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'color')
    # ### end Alembic commands ###