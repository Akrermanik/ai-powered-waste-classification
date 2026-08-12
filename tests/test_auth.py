import pytest

from auth.service import AuthError, hash_password, login_user, register_user, verify_password


def test_registration_and_login():
    result = register_user("auth_user", "Auth User", "StrongPass1")
    assert "access_token" in result
    assert result["user"]["username"] == "auth_user"

    login = login_user("auth_user", "StrongPass1")
    assert login["user"]["name"] == "Auth User"


def test_invalid_login():
    register_user("valid_user", "Valid", "password123")
    with pytest.raises(AuthError):
        login_user("valid_user", "wrong-password")


def test_duplicate_username():
    register_user("dup_user", "Dup", "password123")
    with pytest.raises(AuthError):
        register_user("dup_user", "Dup Two", "otherpass")


def test_password_hashing():
    hashed = hash_password("my-password")
    assert verify_password("my-password", hashed) is True
    assert verify_password("other-password", hashed) is False
