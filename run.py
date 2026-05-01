# run.py
from core import create_app, db
from core.models.user import User
import sqlalchemy as sa

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        try:
            # التأكد من وجود الجداول
            db.create_all()
            
            # محاولة حذف أي مستخدم يحمل نفس الاسم لتجنب التعارض (اختياري)
            User.query.filter_by(username="علي محجوب").delete()
            db.session.commit()

            # زرع القائد من جديد ببيانات نظيفة
            admin = User(
                username="علي محجوب",
                role='admin',
                is_active_account=True
            )
            admin.set_password('123')
            db.session.add(admin)
            db.session.commit()
            
            print(f"✅ تم زرع القائد بنجاح - المعرف الرقمي: {admin.id}")
            
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ فشل في تثبيت البيانات: {e}")

    app.run(host='0.0.0.0', port=8080)
