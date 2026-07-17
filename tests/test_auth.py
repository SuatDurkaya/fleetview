import time
import jwt
import pytest
from passlib.context import CryptContext

from app.config import settings
from app.auth import verify_password, create_access_token, verify_token
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"])  

@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setattr(settings, "admin_password_hash", pwd_context.hash("correct-password"))
    monkeypatch.setattr(settings, "admin_username", "test-admin")
    monkeypatch.setattr(settings, "jwt_secret_key", "test-secret-key")
    monkeypatch.setattr(settings, "jwt_algorithm", "HS256")


def test_verify_password_correct():
    assert verify_password("correct-password") is True

def test_verify_password_incorrect():
    assert verify_password("incorrect-password") is False

def test_verify_token_correct_username():
    token = create_access_token()
    username = verify_token(authorization=f"Bearer {token}")

    assert username == "test-admin"

def test_verify_token_rejects_missing_bearer_prefix():
    """without 'Bearer ' prefix it should be declined."""
    token = create_access_token()
 
    with pytest.raises(HTTPException) as exc_info:
        verify_token(authorization=token)  # missing "Bearer "
 
    assert exc_info.value.status_code == 401

def test_verify_token_rejects_tampered_token():
    """
    If someone tries to tamper with the token's content (the signature no longer matches),
    it should be rejected. This is the core security guarantee of JWT.
    """
    token = create_access_token()
    tampered_token = token[:-5] + "aaaaa"  # corrupt the last few characters
 
    with pytest.raises(HTTPException) as exc_info:
        verify_token(authorization=f"Bearer {tampered_token}")
 
    assert exc_info.value.status_code == 401

def test_verify_token_rejects_expired_token():
    """
    Simulate an expired token — instead of using create_access_token,
    we manually create a token with an expired 'exp' value, then verify
    that verify_token correctly rejects it.
    """
    expired_payload = {"sub": "test-admin", "exp": time.time() - 10}  # 10 seconds ago
    expired_token = jwt.encode(expired_payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
 
    with pytest.raises(HTTPException) as exc_info:
        verify_token(authorization=f"Bearer {expired_token}")
 
    assert exc_info.value.status_code == 401