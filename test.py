import bcrypt

print(bcrypt.hashpw("1".encode(), salt=bcrypt.gensalt()))