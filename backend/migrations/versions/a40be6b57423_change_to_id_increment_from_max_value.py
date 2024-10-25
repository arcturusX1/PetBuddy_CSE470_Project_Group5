"""change to id, increment from max value

Revision ID: a40be6b57423
Revises: 3a598bdb3c6a
Create Date: 2024-08-06 10:07:12.888356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a40be6b57423'
down_revision = '3a598bdb3c6a'
branch_labels = None
depends_on = None

def upgrade():
    # Manually create the sequence if it doesn't exist
    op.execute('CREATE SEQUENCE IF NOT EXISTS users_id_seq')

    # Set the sequence to the next value after the maximum existing id
    op.execute('SELECT setval(\'users_id_seq\', (SELECT COALESCE(MAX(id), 0) FROM users) + 1)')

    # Set the id column to use the sequence
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id', 
                              existing_type=sa.Integer(), 
                              nullable=False, 
                              server_default=sa.text("nextval('users_id_seq'::regclass)"))

    # Ensure the sequence is owned by the id column
    op.execute('ALTER SEQUENCE users_id_seq OWNED BY users.id')

def downgrade():
    # Remove the default value from the id column
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id', 
                              existing_type=sa.Integer(), 
                              nullable=False, 
                              server_default=None)

    # Drop the sequence
    op.execute('DROP SEQUENCE IF EXISTS users_id_seq')