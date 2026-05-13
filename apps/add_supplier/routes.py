from flask import Blueprint

# تأكد من أن الاسم هنا يطابق ما يحاول النظام استيراده
add_supplier_bp = Blueprint('add_supplier', __name__, template_folder='templates')

@add_supplier_bp.route('/add_supplier')
def add_supplier():
    # كود المسار هنا
    pass
