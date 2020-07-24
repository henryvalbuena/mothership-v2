"""Tests for auth module"""
from unittest.mock import MagicMock, patch

import pytest

from src.auth.auth import (
    AuthError,
    get_token_auth_header,
    check_permissions,
    verify_decode_jwt,
)
from tests.auth0_token import test_token
from tests.conftest import exp_token, get_access, jwks, mocked_request as request

test_token = test_token()


@patch("src.auth.auth.request", request(headers={"Authorization": "Bearer abcd123"}))
def test_get_token():
    """Test getting the auth token from the header"""
    token = get_token_auth_header()

    assert token == "abcd123"


@patch("src.auth.auth.request", request(headers={"bad": "header"}))
def test_get_token_missing_header():
    """Test get token with missing header"""
    with pytest.raises(AuthError) as err:
        get_token_auth_header()

    assert err.value.code == 401
    assert err.value.description == "Missing mandatory headers."


@patch("src.auth.auth.request", request(headers={"Authorization": "no_token"}))
def test_get_token_missing_auth_elements():
    """Test get token with missing authorization elements"""
    with pytest.raises(AuthError) as err:
        get_token_auth_header()

    assert err.value.code == 401
    assert err.value.description == "Missing authorization elements."


@patch("src.auth.auth.request", request(headers={"Authorization": "wrong abcd123"}))
def test_get_token_missing_bearer():
    """Test get token with missing bearer keyword"""
    with pytest.raises(AuthError) as err:
        get_token_auth_header()

    assert err.value.code == 401
    assert err.value.description == "Unable to find appropiate keywords."


def test_check_permissions():
    """Test check permissions"""
    res = check_permissions("get:latte", {"permissions": ["get:latte"]})

    assert res is True


def test_check_permissions_missing_key():
    """Test check permissions when permission is missing"""
    with pytest.raises(AuthError) as err:
        check_permissions("get:latte", {"bad": "key"})

    assert err.value.code == 401
    assert err.value.description == "Missing mandatory key."


def test_check_permissions_no_access():
    """Test check permissions when there is no match"""
    with pytest.raises(AuthError) as err:
        check_permissions("get:latte", {"permissions": "nothing_here"})

    assert err.value.code == 401
    assert err.value.description == "User don't have access to resource."


@patch("src.auth.auth.urlopen", MagicMock())
@patch("src.auth.auth.json", MagicMock(method="loads", **jwks))
def test_verify_decode_jwt():
    """Test decode jwt"""
    res = verify_decode_jwt(test_token)
    assert "iss" in res
    assert "sub" in res
    assert "aud" in res
    assert "exp" in res
    assert "permissions" in res
    assert "get:latte" in res["permissions"]
    assert "post:latte" in res["permissions"]
    assert "delete:latte" in res["permissions"]
    assert "patch:latte" in res["permissions"]


@patch("src.auth.auth.urlopen", MagicMock())
@patch("src.auth.auth.json", MagicMock(method="loads", **jwks))
def test_verify_decode_jwt_malformed_header():
    """Test decode jwt when the token header is malformed"""
    with pytest.raises(AuthError) as err:
        verify_decode_jwt("12345asdf")

    assert err.value.code == 401
    assert err.value.description == "Malformed header value."


@patch("src.auth.auth.urlopen", MagicMock())
@patch("src.auth.auth.json", MagicMock(method="loads", **jwks))
def test_verify_decode_jwt_malformed_authorization():
    """Test decode jwt when the token authorization is malformed"""
    with pytest.raises(AuthError) as err:
        verify_decode_jwt(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3OD"
            "kwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJwZXJtaX"
            "NzaW9ucyI6WyJnZXQ6bGF0dGUiLCJwb3N0OmxhdHRlIiwicGF0Y2g6bGF0dG"
            "UiLCJkZWxldGU6bGF0dGUiXX0.uPZwwhHdd6FtMFNU-xmkSzWNiE9-S0szTQkT7a6m0ss"
        )

    assert err.value.code == 401
    assert err.value.description == "Authorization malformed."


@patch("src.auth.auth.urlopen", MagicMock())
@patch("src.auth.auth.json", MagicMock(method="loads", **jwks))
def test_verify_decode_jwt_expired():
    """Test decode jwt when the token has expired"""
    with pytest.raises(AuthError) as err:
        verify_decode_jwt(exp_token)

    assert err.value.code == 401
    assert err.value.description == "Token expired."


@patch("src.auth.auth.urlopen", MagicMock())
@patch("src.auth.auth.json", MagicMock(method="loads", **jwks))
@patch("src.auth.auth.API_AUDIENCE", "derps")
def test_verify_decode_jwt_bad_claims():
    """Test decode jwt when the token has an incorrect audience"""
    with pytest.raises(AuthError) as err:
        verify_decode_jwt(test_token)

    assert err.value.code == 401
    assert (
        err.value.description
        == "Incorrect claims. Please, check the audience and issuer."
    )


@patch("src.auth.auth.urlopen", MagicMock())
@patch("src.auth.auth.json", MagicMock(method="loads", **jwks))
@patch("src.auth.auth.ALGORITHMS", "HS256")
def test_verify_decode_jwt_error_parsing():
    """Test decode jwt when the token cannot be parsed"""
    with pytest.raises(AuthError) as err:
        verify_decode_jwt(test_token)

    assert err.value.code == 400
    assert err.value.description == "Unable to parse authentication token."


@patch("src.auth.auth.urlopen", MagicMock())
@patch("src.auth.auth.json", MagicMock())
def test_verify_decode_jwt_bad_jwks():
    """Test decode jwt when the token is bad"""
    with pytest.raises(AuthError) as err:
        verify_decode_jwt(test_token)

    assert err.value.code == 400
    assert err.value.description == "Unable to find the appropriate key."


@patch(
    "src.auth.auth.request", request(headers={"Authorization": f"Bearer {test_token}"})
)
@patch("src.auth.auth.urlopen", MagicMock())
@patch("src.auth.auth.json", MagicMock(method="loads", **jwks))
def test_auth_decorator():
    """Test auth decorator sucesss"""
    res = get_access("get:latte")()

    assert "iss" in res
    assert "sub" in res
    assert "aud" in res
    assert "exp" in res
    assert "permissions" in res
    assert "get:latte" in res["permissions"]
    assert "post:latte" in res["permissions"]
    assert "delete:latte" in res["permissions"]
    assert "patch:latte" in res["permissions"]

    res = get_access("delete:latte")()

    assert "iss" in res
    assert "sub" in res
    assert "aud" in res
    assert "exp" in res
    assert "permissions" in res
    assert "get:latte" in res["permissions"]
    assert "post:latte" in res["permissions"]
    assert "delete:latte" in res["permissions"]
    assert "patch:latte" in res["permissions"]

    res = get_access("post:latte")()

    assert "iss" in res
    assert "sub" in res
    assert "aud" in res
    assert "exp" in res
    assert "permissions" in res
    assert "get:latte" in res["permissions"]
    assert "post:latte" in res["permissions"]
    assert "delete:latte" in res["permissions"]
    assert "patch:latte" in res["permissions"]


@patch(
    "src.auth.auth.request", request(headers={"Authorization": f"Bearer {test_token}"})
)
@patch("src.auth.auth.urlopen", MagicMock())
@patch("src.auth.auth.json", MagicMock(method="loads", **jwks))
def test_auth_decorator_wrong_permission():
    """Test auth decorator when permission is wrong"""
    with pytest.raises(AuthError) as err:
        get_access("get:drink")()

    assert err.value.code == 401
    assert err.value.description == "User don't have access to resource."


@patch(
    "src.auth.auth.request", request(headers={"Authorization": f"Bearer {test_token}"})
)
@patch("src.auth.auth.urlopen", MagicMock())
@patch("src.auth.auth.json", MagicMock(method="loads", **jwks))
def test_auth_decorator_no_permissions():
    """Test auth decorator when no permissions are supplied"""
    with pytest.raises(AuthError) as err:
        get_access("")()

    assert err.value.code == 401
    assert err.value.description == "User don't have access to resource."


@patch("src.auth.auth.request", request(headers={}))
@patch("src.auth.auth.urlopen", MagicMock())
@patch("src.auth.auth.json", MagicMock(method="loads", **jwks))
def test_auth_decorator_no_header():
    """Test auth decorator when no permissions are supplied"""
    with pytest.raises(AuthError) as err:
        get_access("get:drink")()

    assert err.value.code == 401
    assert err.value.description == "Missing mandatory headers."


@patch(
    "src.auth.auth.request", request(headers={"Authorization": f"Bearer {test_token}"})
)
@patch("src.auth.auth.urlopen", MagicMock())
@patch("src.auth.auth.json", MagicMock(method="loads", **jwks))
def test_auth_decorator_permission_put():
    """Test auth decorator when permissions are put"""
    with pytest.raises(AuthError) as err:
        get_access("put:latte")()

    assert err.value.code == 401
    assert err.value.description == "User don't have access to resource."
