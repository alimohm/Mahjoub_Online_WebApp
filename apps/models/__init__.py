# apps/__init__.py (تأكد من هذا الترتيب)
from flask import Flask
from apps.extensions import db

def create_app():
    app = Flask(__name__)
    db.init_app(app) # تهيئة القاعدة أولاً
    
    with app.app_context():
        # الآن استورد النماذج ليتم تسجيلها في db
        from apps.models import Wallet, WalletTransaction, AdminUser
        db.create_all()
        
    return app
