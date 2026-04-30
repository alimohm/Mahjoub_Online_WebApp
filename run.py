import os
from core import create_app

app = create_app()

if __name__ == "__main__":
    # سيأخذ المنفذ 8080 من إعدادات Railway أو يستخدم 5000 محلياً
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
