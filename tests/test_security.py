"""JWT and password-hashing helpers."""
import jwt
import pytest

from app import config
from app.utils.security import create_access_token, decode_access_token


def test_token_roundtrip():
    assert decode_access_token(create_access_token("user123")) == "user123"


def test_tampered_token_rejected():
    token = create_access_token("user123")
    assert decode_access_token(token[:-3] + ("abc" if not token.endswith("abc") else "xyz")) is None


def test_garbage_token_rejected():
    assert decode_access_token("not-a-token") is None


def test_expired_token_rejected():
    assert decode_access_token(create_access_token("u", expires_minutes=-1)) is None


def test_token_signed_with_other_secret_rejected():
    forged = jwt.encode({"sub": "u"}, "some-other-secret-value-0123456789-abcdefghij", algorithm=config.JWT_ALGORITHM)
    assert decode_access_token(forged) is None


def test_missing_secret_fails_loudly(monkeypatch):
    monkeypatch.setattr(config, "JWT_SECRET", "")
    with pytest.raises(RuntimeError):
        create_access_token("u")


TEMPLATE = "mongodb+srv://t11550788_db_user:<password>@cluster0.example.mongodb.net/?retryWrites=true"


def test_mongo_password_prompt_and_url_encoding(monkeypatch):
    import builtins
    import sys

    monkeypatch.setattr(config, "MONGODB_URI", TEMPLATE)
    monkeypatch.delenv("MONGODB_PASSWORD", raising=False)
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True, raising=False)
    monkeypatch.setattr(builtins, "input", lambda prompt="": "  p@ss#word ")
    uri = config.resolve_mongodb_uri()
    assert "<password>" not in uri and "p%40ss%23word@cluster0" in uri


def test_mongo_password_from_env_and_no_placeholder(monkeypatch):
    monkeypatch.setattr(config, "MONGODB_URI", TEMPLATE)
    monkeypatch.setenv("MONGODB_PASSWORD", "abc123")
    assert ":abc123@" in config.resolve_mongodb_uri()
    monkeypatch.setattr(config, "MONGODB_URI", "mongodb://localhost:27017")
    assert config.resolve_mongodb_uri() == "mongodb://localhost:27017"


def test_mongo_password_missing_without_terminal(monkeypatch):
    import sys

    monkeypatch.setattr(config, "MONGODB_URI", TEMPLATE)
    monkeypatch.delenv("MONGODB_PASSWORD", raising=False)
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False, raising=False)
    with pytest.raises(RuntimeError):
        config.resolve_mongodb_uri()


def test_password_hash_is_not_plaintext_and_verifies():
    pytest.importorskip("bcrypt")
    from app.utils.security import hash_password, verify_password

    hashed = hash_password("my-secret-pw")
    assert hashed != "my-secret-pw"
    assert verify_password("my-secret-pw", hashed)
    assert not verify_password("wrong", hashed)
    assert not verify_password("x", "not-a-valid-hash")
