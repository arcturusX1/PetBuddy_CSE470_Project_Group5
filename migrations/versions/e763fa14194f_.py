"""empty message

Revision ID: e763fa14194f
Revises: cc48f07f2818
Create Date: 2024-07-07 14:57:01.050500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e763fa14194f'
down_revision = 'cc48f07f2818'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prescription', schema=None) as batch_op:
        batch_op.alter_column('med_1',
               existing_type=sa.VARCHAR(),
               nullable=False,
               existing_server_default=sa.text("''::character varying"))
        batch_op.alter_column('med_2',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('test_1',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('test_2',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.drop_constraint('prescription_user_id_key', type_='unique')
        batch_op.drop_constraint('prescription_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])
        batch_op.drop_column('date')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_user', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('is_vet', sa.Boolean(), nullable=False))
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=80),
               existing_nullable=False)
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.drop_constraint('users_email_key', type_='unique')
        batch_op.drop_constraint('users_id_key', type_='unique')
        batch_op.create_unique_constraint(None, ['email'])
        batch_op.create_unique_constraint(None, ['phone'])
        batch_op.drop_column('user_type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_type', sa.BOOLEAN(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint('users_id_key', ['id'])
        batch_op.create_unique_constraint('users_email_key', ['first_name'])
        batch_op.alter_column('phone',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('first_name',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.drop_column('is_vet')
        batch_op.drop_column('is_user')

    with op.batch_alter_table('prescription', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DATE(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('prescription_user_id_fkey', 'users', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
        batch_op.create_unique_constraint('prescription_user_id_key', ['user_id'])
        batch_op.alter_column('test_2',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('test_1',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('med_2',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('med_1',
               existing_type=sa.VARCHAR(),
               nullable=True,
               existing_server_default=sa.text("''::character varying"))

    # ### end Alembic commands ###
