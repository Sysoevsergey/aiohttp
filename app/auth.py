from bcrypt import checkpw, hashpw, gensalt



def hash_password(password: str):
    password = password.encode()
    password = hashpw(password, gensalt())
    password = password.decode()
    return password

def check_password(password_hash_db: str, password_user: str):
    password_hash_db = password_hash_db.encode()
    password_user = password_user.encode()
    return checkpw(password_user, password_hash_db)
