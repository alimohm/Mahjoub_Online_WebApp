# coding: utf-8
# 🛠️ ملف الامتدادات المركزي - منصة محجوب أونلاين 2026
# هذا الملف يضمن عدم حدوث تداخل في الاستيراد (Circular Imports)
# عند استخدام نمط المصنع (Factory Pattern).

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# تهيئة الكائنات (Objects) كحاويات فارغة في البداية
# سيتم ربطها لاحقاً بالتطبيق في ملف apps/__init__.py
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# 💡 توجيه للمطور:
# - لا تقم بربط التطبيق هنا (لا تستخدم .init_app(app) في هذا الملف).
# - استخدم دائماً هذه الكائنات عند تعريف الموديلات (Models) أو المسارات (Routes).
# - الاستيراد الموصى به دائماً: 
#   from apps.extensions import db, login_manager
