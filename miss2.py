from cryptography.fernet import Fernet
import os
import time
import smtplib
from email.message import EmailMessage

KEY_FILE = "generate_key.txt"
DECRYPTED_FILE = "decrypted_file.txt"

def send_email():
    EMAIL_SENDER = "tienhera87@gmail.com"
    EMAIL_RECEIVER = "tienhera87@gmail.com"
    EMAIL_PASSWORD = "uzrh mhzw mqjg rmyy"

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "Email gui noi dung mat ma!"
    msg.set_content("Day la file mat ma duoc gui tu Python!")

    if os.path.exists(DECRYPTED_FILE):
        with open(DECRYPTED_FILE, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(DECRYPTED_FILE)

        msg.add_attachment(file_data, maintype = "plain", subtype = "text", filename = file_name)
        print("Mail da dinh kem file!")
    else:
        print("Khong tim thay file!")
        return

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("Loi khi gui Email!", e)

def save_decrypted_file(content):
    if os.path.exists(DECRYPTED_FILE):
        os.remove(DECRYPTED_FILE)
    with open(DECRYPTED_FILE, "ab") as f:
        f.write(content + b"\n")

def get_or_create_generated_file():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            key = f.read().strip()
        try:
            Fernet(key)
            print("Da doc duoc file key co san!")
            return key
        except ValueError:
            os.remove(KEY_FILE)
            print("File key bi loi, xoa di tao moi!")
    
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print("File key da duoc tao!")
    return key
    
key = get_or_create_generated_file()
f = Fernet(key)

my_secret = "My girlfriend name is Anh Ngu"
hide_secret = my_secret.encode()

token = f.encrypt(hide_secret)

while True:
    user_IO = input("Key de mo khoa mat ma la: ")

    if user_IO.encode() == key:
        time.sleep(0.5)
        print("Mat ma duoc giau kin la:", f.decrypt(token).decode())
        save_decrypted_file(f.decrypt(token))
        send_email()
        print("Mail da duoc gui!")
        break
    else:
        print("Mat ma chua dung, vui long nhap lai Key!")
        time.sleep(0.5)
        continue