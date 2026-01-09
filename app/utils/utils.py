from passlib.context import CryptContext

pass_context = CryptContext(schemes=['bcrypt'],deprecated = "auto")

def password_hashed(password):
    hash_password = pass_context.hash(password)
    return hash_password

def verify_hashed_password(plain_password,hashed_password):
    return pass_context.verify(plain_password,hashed_password)
