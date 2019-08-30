from werkzeug.security import generate_password_hash

password = 'abc'

hashed_password = generate_password_hash(password)

print(hashed_password)
