from core import create_app, db
import os

app = create_app()

# كود سيادي: إنشاء مستخدم المدير تلقائياً عند أول تشغيل
with app.app_context():
    try:
        from core.models import User
        from werkzeug.security import generate_password_hash
        
        # بيانات الدخول الخاصة بك (يمكنك تغييرها لاحقاً)
        admin_email = "admin@mahjoub.com"
        if not User.query.filter_by(email=admin_email).first():
            admin_user = User(
                email=admin_email,
                password=generate_password_hash("Ali_2026_Secure"),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✨ [SUCCESS] Admin account created: admin@mahjoub.com / Ali_2026_Secure")
    except Exception as e:
        print(f"❌ [ERROR] Could not create admin: {e}")

if __name__ == "__main__":
    # الحصول على المنفذ من السيرفر أو استخدام 8080 افتراضياً
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
