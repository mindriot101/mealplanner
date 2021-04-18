"""empty message

Revision ID: 92c9847fdcb6
Revises: 
Create Date: 2021-04-18 01:38:12.862535

"""
from alembic import op
import sqlalchemy as sa
from mealplanner.uuid_type import UUID


# revision identifiers, used by Alembic.
revision = '92c9847fdcb6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ingredient',
    sa.Column('id', UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('fat', sa.Float(), nullable=True),
    sa.Column('saturated_fat', sa.Float(), nullable=True),
    sa.Column('carbohydrate', sa.Float(), nullable=True),
    sa.Column('protein', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ingredient')
    # ### end Alembic commands ###
