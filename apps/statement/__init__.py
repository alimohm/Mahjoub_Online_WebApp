from flask import Blueprint

statement_blueprint = Blueprint(
    'statement_ops', 
    __name__, 
    template_folder='templates'
)

from apps.statement import routes
