import os
from flask import render_template, request, jsonify, url_for, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

# 1. استيراد كائن قاعدة البيانات من الملف الرئيسي
from models.admin_db import db

# 2. استيراد الموديلات من ملفاتها الحقيقية (حسب ما أرسلت)
from models.supplier_db import Supplier
# إذا كان User في ملف admin_db اتركه، وإذا كان في ملف آخر مثل user_db فغير المسار هنا:
try:
    from models.admin_db import User
except ImportError:
    # هذا مجرد تخمين لمكان ملف User إذا لم يكن في admin_db
    from models.user_db import User 

from . import admin_suppliers

@admin_suppliers.route('/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        try:
            # ... كود استقبال البيانات كما هو ...
            username = request.form.get('username')
            # فحص التكرار باستخدام الكلاس المستورد بشكل صحيح
            user_exists = User.query.filter_by(username=username).first()
            # ... باقي منطق الحفظ ...
            
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'تم الاعتماد بنجاح'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 500

    next_id = Supplier.query.count() + 1
    return render_template('admin/add_supplier.html', next_id=next_id)
