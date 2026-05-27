# coding: utf-8
# 🛠️ ملف الامتدادات المركزي - منصة محجوب أونلاين 2026
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# تهيئة الامتدادات (بدون ربطها بالتطبيق حالياً)
# هذا هو التصميم الصحيح لنمط المصنع (Factory Pattern)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# ملاحظة: 
# عند الحاجة لاستخدام قاعدة البيانات أو إدارة المستخدمين في أي ملف،
# استخدم دائماً: 
# from apps.extensions import db, login_manager
