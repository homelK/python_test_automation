import os

from werkzeug.security import generate_password_hash, check_password_hash

dir = os.path.relpath(os.path.dirname("static/files/"))
print(dir)

passw_hash = generate_password_hash("123", "pbkdf2", 8)
check_passw = check_password_hash("pbkdf2:sha256:600000$UHPj66oh$cc3dc47a36495252a0ad94d03f1760d8e834385dcafad1be5211b1305010a98a", "123")

if check_passw:
    print("Match")
