"""empty message

Revision ID: 1add1630a199
Revises: 1e157265b624
Create Date: 2025-02-09 18:14:09.621396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1add1630a199'
down_revision = '1e157265b624'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favourite__planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('favourite__planets_planets_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'planets', ['planet_id'], ['id'])
        batch_op.drop_column('planets_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favourite__planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planets_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favourite__planets_planets_id_fkey', 'planets', ['planets_id'], ['id'])
        batch_op.drop_column('planet_id')

    # ### end Alembic commands ###
