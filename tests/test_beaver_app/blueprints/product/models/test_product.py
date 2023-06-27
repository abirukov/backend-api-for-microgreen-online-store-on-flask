from beaver_app.blueprints.product.models import Product


def test__product_get_search_params():
    assert Product.get_search_fields() == [
        'title',
        'description',
    ]
