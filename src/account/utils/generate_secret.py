import secrets


def generate_token(number_bytes: int = 32) -> str:
    return secrets.token_urlsafe(number_bytes)
