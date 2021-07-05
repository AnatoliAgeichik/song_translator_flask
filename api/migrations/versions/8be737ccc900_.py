"""empty message

Revision ID: 8be737ccc900
Revises: 
Create Date: 2021-07-05 17:30:28.316872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8be737ccc900'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('singer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('track',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('original_language', sa.String(length=2), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=200), nullable=True),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('track_singers',
    sa.Column('Singer_id', sa.Integer(), nullable=True),
    sa.Column('Track_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Singer_id'], ['singer.id'], ),
    sa.ForeignKeyConstraint(['Track_id'], ['track.id'], )
    )
    op.create_table('translation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('track_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.Column('auto_translate', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['track_id'], ['track.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('translation')
    op.drop_table('track_singers')
    op.drop_table('user')
    op.drop_table('track')
    op.drop_table('singer')
    # ### end Alembic commands ###
