from beaver_app.blueprints.category.models import Category


def test__category_get_search_params():
    assert Category.get_search_params() == ['title']
