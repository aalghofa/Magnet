"""empty message

Revision ID: 470ebcca6be2
Revises: 79b3618d99c6
Create Date: 2016-10-20 21:06:27.352055

"""

# revision identifiers, used by Alembic.
revision = '470ebcca6be2'
down_revision = '79b3618d99c6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('ssn', sa.Integer(), nullable=True))
    op.drop_column('employee', 'DOB')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('DOB', sa.DATE(), nullable=True))
    op.drop_column('employee', 'ssn')
    ### end Alembic commands ###
