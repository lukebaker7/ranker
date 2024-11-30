"""item update

Revision ID: 1c9852c5cf1d
Revises: f3a4fda6587b
Create Date: 2024-11-28 20:06:40.407255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c9852c5cf1d'
down_revision = 'f3a4fda6587b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.alter_column('photo_url',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.drop_constraint('_name_description_uc', type_='unique')
        batch_op.drop_index('ix_item_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.create_index('ix_item_name', ['name'], unique=False)
        batch_op.create_unique_constraint('_name_description_uc', ['name', 'description'])
        batch_op.alter_column('photo_url',
               existing_type=sa.TEXT(),
               nullable=True)

    # ### end Alembic commands ###
