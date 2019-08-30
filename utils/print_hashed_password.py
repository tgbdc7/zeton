from werkzeug.security import generate_password_hash

password = 'child_password'

hashed_password = generate_password_hash(password)

print(hashed_password)
