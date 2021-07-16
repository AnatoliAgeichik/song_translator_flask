"""create tables with timestamp

Revision ID: 401747e786d9
Revises: 
Create Date: 2021-07-16 11:51:12.021897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "401747e786d9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("created_timestamp", sa.DateTime(), nullable=False),
        sa.Column(
            "update_timestamp",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_id", sa.String(length=200), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("password", sa.String(length=200), nullable=False),
        sa.Column("admin", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "singer",
        sa.Column("created_timestamp", sa.DateTime(), nullable=False),
        sa.Column(
            "update_timestamp",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "track",
        sa.Column("created_timestamp", sa.DateTime(), nullable=False),
        sa.Column(
            "update_timestamp",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("original_language", sa.String(length=2), nullable=True),
        sa.Column("singer_id", sa.Integer(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["singer_id"],
            ["singer.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "track_singers",
        sa.Column("singer_id", sa.Integer(), nullable=True),
        sa.Column("track_id", sa.Integer(), nullable=True),
        sa.Column("create_timestamp", sa.DateTime(), nullable=False),
        sa.Column(
            "update_timestamp",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["singer_id"],
            ["singer.id"],
        ),
        sa.ForeignKeyConstraint(
            ["track_id"],
            ["track.id"],
        ),
    )
    op.create_table(
        "translation",
        sa.Column("created_timestamp", sa.DateTime(), nullable=False),
        sa.Column(
            "update_timestamp",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("track_id", sa.Integer(), nullable=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("language", sa.CHAR(length=2), nullable=False),
        sa.Column("auto_translate", sa.Boolean(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["track_id"],
            ["track.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("translation")
    op.drop_table("track_singers")
    op.drop_table("track")
    op.drop_table("singer")
    op.drop_table("user")
    # ### end Alembic commands ###
