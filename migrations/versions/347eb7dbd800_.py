"""empty message

Revision ID: 347eb7dbd800
Revises: 70be35608a59
Create Date: 2024-07-09 11:21:43.082531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '347eb7dbd800'
down_revision = '70be35608a59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vets', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_constraint('vets_user_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vets', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('vets_user_id_fkey', 'users', ['user_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###