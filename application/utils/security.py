import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed: bytes = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())
