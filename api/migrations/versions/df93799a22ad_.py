"""empty message

Revision ID: df93799a22ad
Revises: 0618a0517021
Create Date: 2021-07-15 13:16:15.902228

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "df93799a22ad"
down_revision = "0618a0517021"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "track_singers", sa.Column("create_timestamp", sa.DateTime(), nullable=False)
    )
    op.alter_column(
        "track_singers", "singer_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "track_singers", "track_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.drop_column("track_singers", "created_timestamp")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "track_singers",
        sa.Column(
            "created_timestamp",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.alter_column(
        "track_singers", "track_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column(
        "track_singers", "singer_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.drop_column("track_singers", "create_timestamp")
    # ### end Alembic commands ###