"""empty message

Revision ID: 0af57740011b
Revises: 231e522ba12d
Create Date: 2022-01-22 21:36:44.604078

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0af57740011b'
down_revision = '231e522ba12d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pet',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('modify_time', sa.DateTime(), nullable=True),
    sa.Column('is_delete', sa.Integer(), nullable=True),
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('extend', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('category', sa.Integer(), nullable=True),
    sa.Column('size', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pet')
    # ### end Alembic commands ###
