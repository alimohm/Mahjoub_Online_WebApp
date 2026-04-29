import os
from core import create_app

app = create_app()

if __name__ == "__main__":
    # Render يمرر المنفذ عبر متغير البيئة PORT
    port = int(os.environ.get("PORT", 5000))
    # host="0.0.0.0" ضروري للسماح بالاتصالات الخارجية في Render
    app.run(host="0.0.0.0", port=port)
