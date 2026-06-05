from apps.wallet.routes import wallet_app
app.register_blueprint(wallet_app, url_prefix='/wallet')
