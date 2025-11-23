import os
from cryptography.fernet import Fernet

key = os.getenv("ENCRYPTION_KEY", default='123')
fernet = Fernet(key.encode())


def encrypt_data(data: str) -> str:
    if data is None:
        return None
    data = str(data)
    return fernet.encrypt(data.encode()).decode()


def decrypt_data(encrypted: str) -> str:
    if encrypted is None:
        return
    return fernet.decrypt(encrypted.encode()).decode()
