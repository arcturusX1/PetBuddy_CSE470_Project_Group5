"""created vetAvailability class to store availability data

Revision ID: 086239033feb
Revises: 5d3aab20e24f
Create Date: 2024-08-31 18:09:50.394354

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '086239033feb'
down_revision = '5d3aab20e24f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vets', schema=None) as batch_op:
        batch_op.drop_column('availability')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('availability', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
