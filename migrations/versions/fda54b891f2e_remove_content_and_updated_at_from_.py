"""remove content and updated at from vector_articles

Revision ID: fda54b891f2e
Revises: 9e55d13ded1d
Create Date: 2024-05-30 16:32:58.903690

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fda54b891f2e'
down_revision = '9e55d13ded1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vector_articles', schema=None) as batch_op:
        batch_op.drop_column('content')
        batch_op.drop_column('updated_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vector_articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('content', sa.TEXT(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
