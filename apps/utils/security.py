# coding: utf-8
from cryptography.fernet import Fernet
from flask import current_app

class AESCipher:
    """
    كلاس آمن ومبسط باستخدام خوارزمية Fernet (AES-128 مع HMAC)
    تضمن حماية البيانات والتحقق من عدم التلاعب بها.
    """

    @staticmethod
    def _get_fernet():
        # استخدام ENCRYPTION_KEY المخصص للتشفير حصراً
        key = current_app.config.get('ENCRYPTION_KEY')
        if not key:
            raise RuntimeError("⚠️ خطأ أمني: ENCRYPTION_KEY غير مضبوط في إعدادات التطبيق!")
        return Fernet(key.encode())

    @classmethod
    def encrypt(cls, raw_text):
        if not raw_text:
            return None
        try:
            f = cls._get_fernet()
            return f.encrypt(str(raw_text).encode()).decode('utf-8')
        except Exception as e:
            print(f"Encryption error: {e}")
            return None

    @classmethod
    def decrypt(cls, cipher_text):
        if not cipher_text:
            return None
        try:
            f = cls._get_fernet()
            return f.decrypt(cipher_text.encode()).decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
