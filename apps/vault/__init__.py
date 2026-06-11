
# 📂 apps/vault/__init__.py
from flask import Blueprint

vault_bp = Blueprint(
    'vault_bp', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

from apps.vault import routes
