"""Add unique contraint on name/desc

Revision ID: 69b4d3c2ad58
Revises: 622bdb5f87cd
Create Date: 2024-11-28 11:54:08.350523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69b4d3c2ad58'
down_revision = '622bdb5f87cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_index('ix_item_name')
        batch_op.create_index(batch_op.f('ix_item_name'), ['name'], unique=False)
        batch_op.create_unique_constraint('_name_description_uc', ['name', 'description'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_constraint('_name_description_uc', type_='unique')
        batch_op.drop_index(batch_op.f('ix_item_name'))
        batch_op.create_index('ix_item_name', ['name'], unique=1)

    # ### end Alembic commands ###