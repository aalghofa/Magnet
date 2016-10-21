"""empty message

Revision ID: 79b3618d99c6
Revises: None
Create Date: 2016-10-20 09:48:58.536697

"""

# revision identifiers, used by Alembic.
revision = '79b3618d99c6'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('DOB', sa.Date(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('employee', 'DOB')
    ### end Alembic commands ###
