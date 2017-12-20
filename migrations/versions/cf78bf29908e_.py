"""empty message

Revision ID: cf78bf29908e
Revises: 0570a7d79dd7
Create Date: 2017-12-20 11:30:22.496884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf78bf29908e'
down_revision = '0570a7d79dd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phoneNumber',
               existing_type=sa.VARCHAR(length=14),
               nullable=True)
    op.drop_constraint('users_phoneNumber_key', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('users_phoneNumber_key', 'users', ['phoneNumber'])
    op.alter_column('users', 'phoneNumber',
               existing_type=sa.VARCHAR(length=14),
               nullable=False)
    # ### end Alembic commands ###
