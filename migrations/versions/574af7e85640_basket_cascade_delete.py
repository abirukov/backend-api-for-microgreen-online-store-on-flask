"""basket cascade delete

Revision ID: 574af7e85640
Revises: 91a1cde62293
Create Date: 2023-06-18 10:35:18.596646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '574af7e85640'
down_revision = '91a1cde62293'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('basket_products_basket_id_fkey', 'basket_products', type_='foreignkey')
    op.drop_constraint('basket_products_product_id_fkey', 'basket_products', type_='foreignkey')
    op.create_foreign_key(None, 'basket_products', 'products', ['product_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'basket_products', 'baskets', ['basket_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'basket_products', type_='foreignkey')
    op.drop_constraint(None, 'basket_products', type_='foreignkey')
    op.create_foreign_key('basket_products_product_id_fkey', 'basket_products', 'products', ['product_id'], ['id'])
    op.create_foreign_key('basket_products_basket_id_fkey', 'basket_products', 'baskets', ['basket_id'], ['id'])
    # ### end Alembic commands ###
