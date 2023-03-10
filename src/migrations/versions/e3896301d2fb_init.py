"""init

Revision ID: e3896301d2fb
Revises: 
Create Date: 2023-01-25 15:24:46.826691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3896301d2fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('conversion_histories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(asdecimal=True), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.Column('time_of_conversion', sa.DateTime(timezone=True), nullable=False),
    sa.Column('from_currency', sa.String(length=3), nullable=False),
    sa.Column('to_currency', sa.String(length=3), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('conversion_histories')
    # ### end Alembic commands ###
