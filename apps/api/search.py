# 📂 apps/api/search.py
from flask import Blueprint, request, jsonify
from apps.models.supplier_db import Supplier

# تم تعريف الـ Blueprint باسم api_search
api_search = Blueprint('api_search', __name__)

# هذا المسار سيصبح: /api/search
@api_search.route('/search', methods=['GET']) 
def search_suppliers():
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({"results": []})

    # البحث باستخدام ilike (غير حساس لحالة الأحرف)
    # ملاحظة: تأكد أن الأعمدة search_name و search_phone موجودة في موديل Supplier
    suppliers = Supplier.query.filter(
        (Supplier.search_name.ilike(f'%{query}%')) | 
        (Supplier.search_phone.ilike(f'%{query}%'))
    ).limit(10).all()

    results = [
        {
            "id": s.id,
            "name": s.trade_name, 
            "phone": s.owner_phone
        } for s in suppliers
    ]

    return jsonify({"results": results})
