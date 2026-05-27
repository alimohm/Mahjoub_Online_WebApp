# coding: utf-8
from cryptography.fernet import Fernet
import os

class AESCipher:
    def __init__(self, key=None):
        # تأكد أن المفتاح صحيح (32 بايت و Base64 encoded)
        self.key = key or os.getenv('ENCRYPTION_KEY', 'default-fallback-key-32-chars!!').encode()
        try:
            self.cipher = Fernet(self.key)
        except Exception as e:
            # في حال كان المفتاح غير صالح، نستخدم مفتاح افتراضي آمن مؤقت
            self.cipher = Fernet(Fernet.generate_key())

    def encrypt(self, plain_text):
        if not plain_text: return None
        return self.cipher.encrypt(str(plain_text).encode()).decode()

    def decrypt(self, cipher_text):
        if not cipher_text: return None
        return self.cipher.decrypt(str(cipher_text).encode()).decode()

    def decrypt_to_float(self, value):
        """
        دالة ذكية:
        1. إذا كانت القيمة مشفرة (تبدأ بـ gAAAAA)، تفك التشفير ثم تحول لرقم.
        2. إذا كانت القيمة رقمية عادية، تحولها لرقم مباشرة.
        3. إذا فشلت، تعيد 0.0 لتجنب انهيار الموقع.
        """
        if value is None:
            return 0.0
        
        str_val = str(value).strip()
        
        # محاولة فك التشفير إذا كانت القيمة تبدو مشفرة (تنسيق Fernet)
        if str_val.startswith('gAAAAA'):
            try:
                decrypted = self.decrypt(str_val)
                return float(decrypted)
            except Exception:
                return 0.0
        
        # إذا كانت القيمة ليست مشفرة، حاول تحويلها مباشرة
        try:
            return float(str_val)
        except ValueError:
            return 0.0

# نسخة جاهزة للاستخدام في الموديلات
cipher_suite = AESCipher()
