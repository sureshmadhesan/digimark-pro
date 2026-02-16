from app.core.security import decrypt_secret, encrypt_secret


def test_encrypt_decrypt_roundtrip():
    text = "sensitive-token"
    encrypted = encrypt_secret(text)
    assert encrypted != text
    assert decrypt_secret(encrypted) == text
