from beaver_app.blueprints.category.models import Category


def test__category_get_search_fields():
    assert Category.get_search_fields() == ['title']

