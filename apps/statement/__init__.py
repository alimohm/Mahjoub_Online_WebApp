from flask import Blueprint

# تأكد أن الاسم هنا هو 'statement_blueprint'
statement_blueprint = Blueprint(
    'statement_blueprint', 
    __name__, 
    template_folder='templates'
)

from apps.statement import routes
