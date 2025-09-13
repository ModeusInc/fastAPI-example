from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_generator(password: str):
    return pwd_context.hash(password)


def verify(regular_password, hashed_password):
    return pwd_context.verify(regular_password, hashed_password)
