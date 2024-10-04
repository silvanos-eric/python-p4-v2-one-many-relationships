"""add column employee_id to onboardings table

Revision ID: 3b2b183c6941
Revises: a92393123443
Create Date: 2024-10-04 18:18:35.439295

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3b2b183c6941'
down_revision = 'a92393123443'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('onboardings') as batch_op:
        batch_op.add_column(sa.Column('employee_id', sa.Integer,
                                      nullable=True))
        batch_op.create_foreign_key(
            'fk_onboardings_employee_id_employees',  # Foreign key name
            'employees',  # Referent table
            ['employee_id'],  # Column in the current table
            ['id'])  # Column in the  referent table
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_onboardings_employee_id_employees'),
                       'onboardings',
                       type_='foreignkey')
    op.drop_column('onboardings', 'employee_id')
    with op.batch_alter_table('onboardings') as batch_op:
        batch_op.drop_constraint('fk_onboardings_employee_id_employees',
                                 type_='foreignkey')
        batch_op.drop_column('employee_id')
    # ### end Alembic commands ###
