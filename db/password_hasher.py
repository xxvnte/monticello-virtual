import bcrypt

BCRYPT_ROUNDS = 12


def hash_password(plain_password):
    encoded = plain_password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    return bcrypt.hashpw(encoded, salt).decode("utf-8")


def verify_password(plain_password, stored_hash):
    if not stored_hash:
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            stored_hash.encode("utf-8"),
        )
    except ValueError:
        return False
