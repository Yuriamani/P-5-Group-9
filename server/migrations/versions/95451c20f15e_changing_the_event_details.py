"""changing the event details

Revision ID: 95451c20f15e
Revises: d6c55dd92bd9
Create Date: 2024-08-18 17:44:12.705794

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '95451c20f15e'
down_revision = 'd6c55dd92bd9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedback')
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('available_tickets', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('ticket_price', sa.Integer(), nullable=True))
        batch_op.drop_column('normal_tickets')
        batch_op.drop_column('vip_tickets')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vip_tickets', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('normal_tickets', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('ticket_price')
        batch_op.drop_column('available_tickets')

    op.create_table('feedback',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('feedback', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], name='feedback_event_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='feedback_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='feedback_pkey')
    )
    # ### end Alembic commands ###
