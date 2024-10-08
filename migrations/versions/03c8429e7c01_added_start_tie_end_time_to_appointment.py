"""added start_tie, end_time to appointment

Revision ID: 03c8429e7c01
Revises: 575b8f1b0db2
Create Date: 2024-09-09 17:29:52.551811

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '03c8429e7c01'
down_revision = '575b8f1b0db2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_time', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('end_time', sa.DateTime(), nullable=False))
        batch_op.drop_column('date_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.drop_column('end_time')
        batch_op.drop_column('start_time')

    # ### end Alembic commands ###
