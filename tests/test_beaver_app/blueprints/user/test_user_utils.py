from beaver_app.blueprints.user.utils import is_current_user, get_personal_code, generate_personal_code, \
    is_personal_code_uniq


def test_is_current_user_success(saved_user_admin):
    assert is_current_user(
        str(saved_user_admin.id),
        saved_user_admin.id,
    ) is True


def test_get_personal_code():
    code = get_personal_code()
    assert code is not None


def test_generate_personal_code():
    code = generate_personal_code()
    assert len(code) == 4


def test_is_personal_code_uniq_true():
    assert is_personal_code_uniq('KK55') is True


def test_is_personal_code_uniq_false(saved_user_admin):
    assert is_personal_code_uniq(saved_user_admin.personal_code) is False
