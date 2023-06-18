from beaver_app.blueprints.basket.models import Basket


def test_get_search_fields():
    assert Basket.get_search_fields() == []
