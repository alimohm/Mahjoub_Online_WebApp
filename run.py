import os
from sqlalchemy import text
from core import create_app, db
from core.models.user import User

app = create_app()

with app.app_context():
    # مسح الجداول القديمة لضمان تحديث الأعمدة (is_active_account)
    db.session.execute(text('DROP TABLE IF EXISTS "user" CASCADE;'))
    db.create_all()
    
    # إضافة القائد "علي محجوب" كأدمن افتراضي
    if not User.query.filter_by(username="علي محجوب").first():
        admin = User(username="علي محجوب", role='admin')
        admin.set_password('123')
        db.session.add(admin)
        db.session.commit()
        print("✅ تم إنشاء حساب القائد بنجاح!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
