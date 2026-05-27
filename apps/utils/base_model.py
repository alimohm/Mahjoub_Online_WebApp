# coding: utf-8
from apps.extensions import db
from flask import current_app

class EncryptedModel(db.Model):
    __abstract__ = True # هذا الكلاس لن ينشئ جدولاً، بل هو قالب للوراثة

    def encrypt_field(self, value):
        return current_app.cipher.encrypt(str(value))

    def decrypt_field(self, encrypted_value):
        return current_app.cipher.decrypt(encrypted_value)
