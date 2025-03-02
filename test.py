import bcrypt

print(bcrypt.hashpw("".encode(), salt=bcrypt.gensalt()))
