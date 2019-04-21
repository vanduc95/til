"""Add a column

Revision ID: 2df29f617d13
Revises: c00c1e2aba90
Create Date: 2018-07-02 09:36:43.861944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2df29f617d13'
down_revision = 'c00c1e2aba90'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))

def downgrade():
    op.drop_column('account', 'last_transaction_date')