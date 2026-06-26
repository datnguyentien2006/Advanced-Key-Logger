from cryptography.fernet import Fernet
import os
import time

def get_or_create_file_key():
    if os.path.exists("generate_key.txt"):
        with open("generate_key.txt", "rb") as f:
            key = f.read().strip()

            try:
                Fernet(key)
                print("Da doc duoc key tu file generate_key.txt")
                return key
            except ValueError:
                print("File tao ra bi loi, xoa file va tao lai")
                os.remove("generate_key.txt")
            
    key = Fernet.generate_key()
    with open("generate_key.txt", "wb") as f:
        f.write(key)
        print("Viet key vao file generate_key.txt moi duoc tao")
        return key
        
key = get_or_create_file_key()
f = Fernet(key)

my_secret = "My girlfriend is Anh Ngu"
hide_secret = my_secret.encode()

token = f.encrypt(hide_secret)

while True:
    user_IO = input("Moi ban nhap dung key de lay mat ma:")

    if user_IO.encode() == key:
        time.sleep(0.5)
        print("Mat ma duoc giau kin do la", f.decrypt(token).decode())
        break
    else:
        print("Mat ma ban dua chua dung, hay thu lai lan nua")
        time.sleep(0.5)
