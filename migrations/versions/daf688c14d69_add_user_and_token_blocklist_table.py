"""add user and token blocklist table

Revision ID: daf688c14d69
Revises: f7cb35c73cd8
Create Date: 2023-05-29 11:42:18.828394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daf688c14d69'
down_revision = 'f7cb35c73cd8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('middle_name', sa.String(), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('tg_id', sa.String(length=255), nullable=True),
    sa.Column('tg_username', sa.String(length=255), nullable=True),
    sa.Column('personal_code', sa.String(length=255), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('inviter_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['inviter_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('personal_code'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('tg_id'),
    sa.UniqueConstraint('tg_username')
    )
    op.create_table('token_blocklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('type', sa.String(length=16), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_token_blocklist_jti'), 'token_blocklist', ['jti'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_token_blocklist_jti'), table_name='token_blocklist')
    op.drop_table('token_blocklist')
    op.drop_table('users')
    # ### end Alembic commands ###