"""add notification

Revision ID: 0aa00cb8de18
Revises: 3e8ba40e9535
Create Date: 2019-05-21 17:35:30.434158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0aa00cb8de18'
down_revision = '3e8ba40e9535'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_name'), 'notifications', ['name'], unique=False)
    op.create_index(op.f('ix_notifications_timestamp'), 'notifications', ['timestamp'], unique=False)
    # op.drop_column('post', 'salman')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.add_column('post', sa.Column('salman', sa.VARCHAR(length=50), nullable=True))
    op.drop_index(op.f('ix_notifications_timestamp'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_name'), table_name='notifications')
    op.drop_table('notifications')
    # ### end Alembic commands ###
