import json
import base64
import hashlib
from flask import Blueprint, render_template, request, jsonify
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import unpad # استخدام مكتبة موثوقة للـ Padding

add_supplier = Blueprint('add_supplier', __name__, template_folder='templates')

SECRET_PASSWORD = "YOUR_SUPER_SECRET_AES_KEY_256"

def decrypt_aes_cryptojs(encrypted_text, password):
    try:
        # 1. تنظيف النص (قد يتم إضافة مسافات زائدة أحياناً)
        encrypted_text = encrypted_text.strip()
        encrypted_data = base64.b64decode(encrypted_text)
        
        if encrypted_data[:8] != b'Salted__':
            raise ValueError("تنسيق التشفير غير مدعوم: لا يوجد Salted")
    
        salt = encrypted_data[8:16]
        ciphertext = encrypted_data[16:]
        
        # 2. اشتقاق المفتاح
        key_iv = PBKDF2(password, salt, 48, count=10000, hmac_hash_module=hashlib.sha256)
        key = key_iv[:32]
        iv = key_iv[32:]
        
        # 3. فك التشفير مع الحماية من الـ Padding
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(ciphertext)
        
        # 4. إزالة الحشوة بشكل آمن
        return unpad(decrypted_data, AES.block_size).decode('utf-8')
    except Exception as e:
        raise Exception(f"فشل فك التشفير: {str(e)}")

@add_supplier.route('/add_supplier_submit', methods=['POST'])
def add_supplier_submit():
    encrypted_payload = request.form.get('full_encrypted_data')
    
    if not encrypted_payload:
        return jsonify({"status": "error", "message": "البيانات فارغة"}), 400

    try:
        decrypted_json = decrypt_aes_cryptojs(encrypted_payload, SECRET_PASSWORD)
        data = json.loads(decrypted_json)
        
        # --- هنا تبدأ عملية التعميد ---
        # مثال: حفظ البيانات في قاعدة البيانات
        # supplier = Supplier(username=data['auth']['username'], ...)
        # db.session.commit()
        
        return jsonify({"status": "success", "message": "تمت معالجة البيانات بنجاح"})
        
    except Exception as e:
        # تسجيل الخطأ في الـ Logs لتسهيل التصحيح
        print(f"CRITICAL ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
