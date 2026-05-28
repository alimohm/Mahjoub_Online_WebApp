import json
import base64
import hashlib
from flask import Blueprint, render_template, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

add_supplier = Blueprint('add_supplier', __name__, template_folder='templates')

# استخدم مفتاحاً ثابتاً بسيطاً لتجنب مشاكل الـ Salt/PBKDF2 مؤقتاً للتأكد من الاستقرار
# في الإنتاج، يجب أن تكون هذه القيمة مخزنة بشكل آمن
SECRET_KEY = "12345678901234567890123456789012" # 32 bytes لـ AES-256

def decrypt_data(encrypted_str):
    """محرك فك التشفير المباشر (AES-CBC)"""
    try:
        # فك تشفير Base64
        raw_data = base64.b64decode(encrypted_str)
        
        # استخراج الـ IV (أول 16 بايت) والبيانات المشفرة
        iv = raw_data[:16]
        ciphertext = raw_data[16:]
        
        # إعداد المحرك
        cipher = AES.new(SECRET_KEY.encode('utf-8'), AES.MODE_CBC, iv)
        
        # فك التشفير وإزالة الـ Padding
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted.decode('utf-8')
    except Exception as e:
        print(f"Error in Decryption: {e}")
        return None

@add_supplier.route('/add_supplier_submit', methods=['POST'])
def add_supplier_submit():
    encrypted_payload = request.form.get('full_encrypted_data')
    
    if not encrypted_payload:
        return jsonify({"status": "error", "message": "لا يوجد بيانات مشفرة"}), 400

    decrypted_json = decrypt_data(encrypted_payload)
    
    if not decrypted_json:
        return jsonify({"status": "error", "message": "فشل فك التشفير - مفتاح غير متطابق أو بيانات تالفة"}), 400

    try:
        data = json.loads(decrypted_json)
        # هنا يمكنك طباعة البيانات للتأكد: print(data)
        
        # قم بعمليات الحفظ في قاعدة البيانات هنا
        
        return jsonify({"status": "success", "message": "تمت معالجة البيانات السيادية بنجاح"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"خطأ في تحليل البيانات: {str(e)}"}), 500

@add_supplier.route('/add_supplier', methods=['GET'])
def render_form():
    return render_template('admin/full_encrypted_supplier_form.html')
