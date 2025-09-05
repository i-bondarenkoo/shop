import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed: bytes = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()
