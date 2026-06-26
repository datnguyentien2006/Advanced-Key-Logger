from cryptography.fernet import Fernet
import os
import time

KEY_FILE = "users_key.txt"
num_users = int(input("Moi nhap so luong nguoi dung: "))

def get_or_load_users():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        valid = True
        for line in lines:
            try:
                Fernet(line)
                continue
            except ValueError:
                valid = False
                break

        if valid and len(lines) == num_users:
            print("KEY DA DUOC TAO SAN!")
            return lines
        else:
            print("FILE KEY BI LOI, XOA DI VA TAI LAI FILE KEY MOI!")
            os.remove(KEY_FILE)

        lines = [Fernet.generate_key() for _ in range(num_users)]
        with open(KEY_FILE, "wb") as f:
            for line in lines:
                f.write(line + b"\n")
        print("FILE KEY DA DUOC TAO!")
        return lines

users_key = get_or_load_users()
users_secret = [input(f"MOi NHAP SECRET CUA USER {i+1}: ") for i in range(num_users)]
combine_users = list(zip(users_key, users_secret))

for i, (key, secret) in enumerate(combine_users, start=1):
    f = Fernet(key)

    hide_secret = str(secret).encode()
    tokens = f.encrypt(hide_secret)

    while True:
        userIO = input(f"MOI USER {i} NHAP KEY: ")
        if userIO.encode() == key:
            print(f"MAT MA DUOC GIAU KIN CUA USER {i}: ", f.decrypt(tokens).decode())
            break
        else:
            print(f"USER {i} DA NHAP SAI KEY \nVUI LONG NHAP LAI! \n")
            continue
