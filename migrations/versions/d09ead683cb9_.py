"""empty message

Revision ID: d09ead683cb9
Revises: 239310959460
Create Date: 2024-08-15 14:03:25.401010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd09ead683cb9'
down_revision = '239310959460'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vets', schema=None) as batch_op:
        batch_op.alter_column('first_name',
               existing_type=sa.TEXT(),
               type_=sa.String(length=80),
               existing_nullable=False,
               existing_server_default=sa.text("''::text"))
        batch_op.alter_column('last_name',
               existing_type=sa.TEXT(),
               type_=sa.String(length=80),
               existing_nullable=False,
               existing_server_default=sa.text("''::text"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vets', schema=None) as batch_op:
        batch_op.alter_column('last_name',
               existing_type=sa.String(length=80),
               type_=sa.TEXT(),
               existing_nullable=False,
               existing_server_default=sa.text("''::text"))
        batch_op.alter_column('first_name',
               existing_type=sa.String(length=80),
               type_=sa.TEXT(),
               existing_nullable=False,
               existing_server_default=sa.text("''::text"))

    # ### end Alembic commands ###
