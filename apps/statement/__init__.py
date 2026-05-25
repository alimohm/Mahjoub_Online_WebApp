from flask import Blueprint

# تغيير الاسم هنا ليكون 'statement_blueprint'
statement_blueprint = Blueprint(
    'statement_blueprint', 
    __name__, 
    template_folder='templates'
)

from apps.statement import routes
