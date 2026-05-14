# coding: utf-8
# ملف التشغيل الرئيسي لمنصة محجوب أونلاين
import os
from flask import Flask

# إنشاء كائن التطبيق - تأكد أن اسمه 'app' ليجده Gunicorn
app = Flask(__name__)

@app.route('/')
def home():
    return "Mahjoub Online is Running!"

if __name__ == "__main__":
    # تشغيل التطبيق على المنفذ الذي تحدده المنصة السحابية
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
