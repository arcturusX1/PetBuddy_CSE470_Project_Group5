"""message for migration

Revision ID: 10f60761fbb6
Revises: a40be6b57423
Create Date: 2024-08-13 14:11:47.271366

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '10f60761fbb6'
down_revision = 'a40be6b57423'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=100), nullable=True))
        batch_op.alter_column('availability',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vets', schema=None) as batch_op:
        batch_op.alter_column('availability',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               nullable=True)
        batch_op.drop_column('name')

    # ### end Alembic commands ###
