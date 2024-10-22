"""empty message

Revision ID: dbf76204046a
Revises: 1b6f59e1bf99
Create Date: 2024-07-07 16:54:55.404198

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbf76204046a'
down_revision = '1b6f59e1bf99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prescription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.alter_column('med_2',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('test_1',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('test_2',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False,
               autoincrement=True)
        batch_op.drop_constraint('users_id_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_unique_constraint('users_id_key', ['id'])
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               server_default=sa.Identity(always=False, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1),
               existing_nullable=False,
               autoincrement=True)

    with op.batch_alter_table('prescription', schema=None) as batch_op:
        batch_op.alter_column('test_2',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('test_1',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('med_2',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.drop_column('id')

    # ### end Alembic commands ###