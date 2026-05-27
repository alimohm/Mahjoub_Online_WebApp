# coding: utf-8
from cryptography.fernet import Fernet
import os

class AESCipher:
    def __init__(self, key=None):
        # الاعتماد على المتغير البيئي أو مفتاح افتراضي
        self.key = key or os.getenv('ENCRYPTION_KEY', 'default-fallback-key-32-chars!!').encode()
        self.cipher = Fernet(self.key)

    def encrypt(self, plain_text):
        return self.cipher.encrypt(plain_text.encode()).decode()

    def decrypt(self, cipher_text):
        return self.cipher.decrypt(cipher_text.encode()).decode()

# لا تقم بإنشاء نسخة هنا، سننشئها داخل الموديلات عند الحاجة
