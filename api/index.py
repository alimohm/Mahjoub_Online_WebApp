from apps import create_app

app = create_app()

# Vercel يحتاج إلى متغير اسمه app
if __name__ == "__main__":
    app.run()
