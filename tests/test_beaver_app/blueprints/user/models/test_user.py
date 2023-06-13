from beaver_app.blueprints.user.models import User


def test__is_admin_by_id__true(saved_user_admin):
    assert User.is_admin_by_id(saved_user_admin.id) is True


def test__is_admin_by_id__false(saved_user_client_first):
    assert User.is_admin_by_id(saved_user_client_first.id) is False


def test__is_admin_by_id__false_no_user(not_existing_uuid):
    assert User.is_admin_by_id(not_existing_uuid) is False


def test__user_get_search_params():
    assert User.get_search_fields() == [
        'first_name',
        'last_name',
        'middle_name',
        'phone',
        'email',
        'tg_id',
        'tg_username',
        'personal_code',
    ]
