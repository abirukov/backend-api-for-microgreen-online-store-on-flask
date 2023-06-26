from beaver_app.blueprints.order.models import Order


def test__order_get_search_params():
    assert Order.get_search_fields() == ['comment', 'address', 'status']
