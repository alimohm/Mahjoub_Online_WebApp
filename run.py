import os
import sys

# 1. تثبيت المسار الجذري للمشروع
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# 2. طباعة للتأكد في الـ Logs
print(f"🚀 [System] Project Root: {PROJECT_ROOT}")
print(f"📁 [System] Contents: {os.listdir(PROJECT_ROOT)}")

try:
    # الاستيراد بعد تثبيت المسارات
    from core import create_app
    app = create_app()
except Exception as e:
    print(f"❌ [Critical] Failed to initialize app: {e}")
    raise e

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
