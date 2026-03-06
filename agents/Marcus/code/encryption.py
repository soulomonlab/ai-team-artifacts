import os
from cryptography.fernet import Fernet

# Key should be set in env: LINKEDIN_ENC_KEY
# If not present, generate one for dev/testing only.
def get_key() -> bytes:
    key = os.getenv("LINKEDIN_ENC_KEY")
    if key:
        return key.encode()
    # DEV fallback (not for production)
    k = Fernet.generate_key()
    return k

fernet = Fernet(get_key())


def encrypt(plaintext: str) -> bytes:
    if plaintext is None:
        return None
    return fernet.encrypt(plaintext.encode())


def decrypt(token_bytes: bytes) -> str:
    if token_bytes is None:
        return None
    return fernet.decrypt(token_bytes).decode()
