from werkzeug.security import generate_password_hash

password = input('Insert password: ')
hashed_password=generate_password_hash(password, "pbkdf2:sha256")
print(hashed_password)