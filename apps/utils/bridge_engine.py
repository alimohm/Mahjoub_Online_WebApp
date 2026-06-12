# coding: utf-8
# 📂 apps/utils/bridge_engine.py - محرك الربط الآلي (Mahjoub Bridge Engine)

import requests
from config import Config

class QumraBridgeEngine:
    def __init__(self):
        # نقطة الاتصال المعتمدة من لوحة تحكم قمرة
        self.endpoint = "https://mahjoub.online/admin/graphql"
        # التوثيق باستخدام مفتاح الربط الموجود في إعدادات التطبيق
        self.headers = {
            "Authorization": f"Bearer {Config.QUMRA_API_KEY}",
            "Content-Type": "application/json"
        }

    def execute_query(self, query, variables=None):
        """تنفيذ استعلام GraphQL وإرساله إلى منصة قمرة."""
        payload = {"query": query, "variables": variables or {}}
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Bridge Engine Error: {e}")
            return {"errors": str(e)}

    def map_product_to_qumra(self, data):
        """
        محول البيانات: يحول القالب الخاص بك إلى هيكل قمرة المطلوب.
        يدعم المنتجات الأساسية، الصور، المتغيرات، وبصمة المورد.
        """
        mutation = """
        mutation CreateProduct($input: ProductInput!) {
            createProduct(input: $input) {
                id
                name
            }
        }
        """
        
        # تجهيز المتغيرات بما يتوافق مع الـ Schema الخاص بقمرة
        # يتم التقاط supplier_id من البيانات الواردة للمطابقة مع البصمة
        variables = {
            "input": {
                "name": data.get('title'),
                "description": data.get('description'),
                "price": float(data.get('price', 0)),
                "quantity": int(data.get('quantity', 0) or 0),
                "image_url": data.get('image_url'),
                "customFields": [
                    {
                        "key": "supplier_id", 
                        "value": str(data.get('supplier_id', 'UNKNOWN'))
                    }
                ],
                "variants": [] # يتم ملؤها إذا توفرت بيانات المتغيرات
            }
        }
        
        # إضافة المتغيرات (Variants) إذا كانت موجودة في القالب
        if data.get('option1_name'):
            variables['input']['variants'].append({
                "price": float(data.get('variant_price', 0)),
                "quantity": int(data.get('variant_quantity', 0) or 0),
                "image_url": data.get('variant_image_url'),
                "options": {
                    data.get('option1_name'): data.get('option1_value'),
                    data.get('option2_name'): data.get('option2_value')
                }
            })
            
        return self.execute_query(mutation, variables)

    def fetch_latest_products(self, limit=10, page=1):
        """جلب آخر 10 منتجات للمزامنة اللحظية في لوحة التحكم."""
        query = """
        query GetProducts($limit: Int, $offset: Int) {
            products(limit: $limit, offset: $offset) {
                title
                price
                customFields { key, value }
            }
        }
        """
        variables = {"limit": limit, "offset": (page - 1) * limit}
        result = self.execute_query(query, variables)
        return result.get('data', {}).get('products', []) if result else []
