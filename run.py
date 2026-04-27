from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from core import app, db  # نفترض أن app و db تم تعريفهما في core/__init__.py
from core.models import User

# 1. استيراد البوابات (Blueprints)
from supplier_panel import supplier_bp
# from admin_panel import admin_bp  # فعلها عند تجهيز لوحة الإدارة

# 2. تسجيل البوابات في النظام
# سيعمل المورد عبر الرابط: mahjoub.online/supplier
app.register_blueprint(supplier_bp, url_prefix='/supplier')

# 3. إعدادات نظام الحماية (Login Manager)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'supplier_panel.login'  # الصفحة الافتراضية عند محاولة الدخول غير المصرح
login_manager.login_message = "يرجى إدخال شفرة العبور للوصول إلى الترسانة."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    # محرك البحث عن المستخدم في قاعدة البيانات السيادية
    return User.query.get(int(user_id))

# 4. توجيه الرابط الرئيسي (الصفحة الرئيسية للموقع)
@app.route('/')
def index():
    # مؤقتاً، سنوجه الزوار إلى بوابة الموردين حتى تنتهي من تصميم المتجر العام
    return redirect(url_for('supplier_panel.login'))

# 5. تشغيل المحرك
if __name__ == '__main__':
    # ملاحظة: في Railway يتم تجاهل debug=True ويستخدم gunicorn
    # لكن نتركها هنا للتطوير المحلي
    app.run(debug=True, host='0.0.0.0', port=5000)
