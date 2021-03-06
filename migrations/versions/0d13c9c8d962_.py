"""empty message

Revision ID: 0d13c9c8d962
Revises: 
Create Date: 2021-04-25 00:13:50.958343

"""
from alembic import op
import sqlalchemy as sa
from mealplanner.uuid_type import UUID


# revision identifiers, used by Alembic.
revision = "0d13c9c8d962"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ingredient",
        sa.Column("id", UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("fat", sa.Float(), nullable=True),
        sa.Column("saturated_fat", sa.Float(), nullable=True),
        sa.Column("carbohydrate", sa.Float(), nullable=True),
        sa.Column("protein", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "recipe",
        sa.Column("id", UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "allocation",
        sa.Column("id", UUID(), nullable=False),
        sa.Column("meal", sa.String(), nullable=False),
        sa.Column("day", sa.String(), nullable=False),
        sa.Column("recipe_id", UUID(), nullable=True),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipe.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "membership",
        sa.Column("id", UUID(), nullable=False),
        sa.Column("ingredient_id", UUID(), nullable=True),
        sa.Column("recipe_id", UUID(), nullable=True),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ingredient_id"], ["ingredient.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipe.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("membership")
    op.drop_table("allocation")
    op.drop_table("recipe")
    op.drop_table("ingredient")
    # ### end Alembic commands ###
