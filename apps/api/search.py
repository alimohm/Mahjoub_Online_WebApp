# 📂 apps/api/search.py - المحرك البرمجي للبحث الذكي
from flask import Blueprint, request, jsonify
from flask_login import login_required
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint
api_search = Blueprint('api_search', __name__)

# هذا المسار المسجل في __init__.py بـ url_prefix='/api'
# لذا الرابط النهائي هو: /api/search
@api_search.route('/search', methods=['GET'])
@login_required
def search_suppliers():
    """
    محرك بحث ذكي يقوم بالاستعلام عن الموردين 
    بناءً على الاسم التجاري أو رقم الهاتف.
    """
    query = request.args.get('q', '').strip()
    
    # إذا كان حقل البحث فارغاً، نرجع قائمة فارغة
    if not query:
        return jsonify({"results": []})

    # المحرك يبحث في قاعدة البيانات
    # ملاحظة: تأكد أن حقول 'trade_name' و 'owner_phone' هي الأسماء الصحيحة في Supplier model
    suppliers = Supplier.query.filter(
        (Supplier.trade_name.ilike(f'%{query}%')) | 
        (Supplier.owner_phone.ilike(f'%{query}%'))
    ).limit(10).all()

    # تجهيز النتائج بتنسيق (id, text) المتوافق مع مكتبة Select2
    results = [
        {
            "id": s.id, 
            "text": f"{s.trade_name} - {s.owner_phone}"
        } 
        for s in suppliers
    ]
    
    return jsonify({"results": results})
