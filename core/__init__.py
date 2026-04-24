from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# تعريف db هنا ليكون متاحاً للمودلز
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)
    
    # تهيئة القاعدة
    db.init_app(app)
    
    with app.app_context():
        # كسر الحلقة الدائرية: الاستيراد داخل الـ context
        try:
            from core import models
            from admin_panel.routes import admin_bp
            from supplier_panel.routes import supplier_bp
            
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ تم تسجيل بوابات الإدارة والموردين بنجاح.")
        except Exception as e:
            print(f"❌ خطأ في الربط: {e}")

    @app.route('/')
    def index():
        return """
        <div style="text-align:center; margin-top:50px; font-family: sans-serif; direction:rtl;">
            <h1 style="color: #6a0dad;">🚀 نظام محجوب أونلاين يعمل بنجاح!</h1>
            <p>المحرك متصل الآن بقاعدة بيانات رندر وبوابة قمرة.</p>
            <div style="margin-top: 30px;">
                <a href="/admin/" style="display:inline-block; padding:15px 30px; background:#6a0dad; color:white; text-decoration:none; border-radius:25px; font-weight:bold;">
                    دخول لوحة الإدارة ⬅️
                </a>
            </div>
        </div>
        """
    return app
