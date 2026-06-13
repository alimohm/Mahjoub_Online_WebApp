# coding: utf-8
# 📂 apps/utils/bridge_engine.py

import requests
from config import Config

class QumraBridgeEngine:
    def __init__(self):
        self.endpoint = "https://mahjoub.online/admin/graphql"
        api_token = getattr(Config, 'QUMRA_API_KEY', '').strip()
        
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://mahjoub.online",
            "Referer": "https://mahjoub.online/admin/"
        }

    def execute_query(self, query, variables=None):
        payload = {"query": query, "variables": variables or {}}
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=15)
            if response.status_code != 200:
                print(f"DEBUG: Status {response.status_code} | Response: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            
            if 'errors' in result:
                print(f"⚠️ GraphQL Errors: {result['errors']}")
            return result.get('data', {})
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")
            return {}

    def fetch_latest_products(self, limit=10, page=1):
        # تم إضافة الحقول: pricing { price } و image_url
        query = """
        query GetProducts($limit: Int, $page: Int) {
            findAllProducts(input: { limit: $limit, page: $page }) {
                data {
                    title
                    quantity
                    image_url
                    pricing {
                        price
                    }
                }
            }
        }
        """
        variables = {"limit": limit, "page": page}
        data = self.execute_query(query, variables)
        
        products = data.get('findAllProducts', {}).get('data', [])
        
        # لا نحتاج إلى generate_product_html إذا كنا سنعتمد على الحقول المباشرة في القالب
        return products if isinstance(products, list) else []

    def generate_product_html(self, product):
        # هذا القالب يستخدم فقط في حال عدم توفر بيانات، يمكنك تركه كإجراء احتياطي
        return f"""<div class="product-snippet"><strong>{product.get('title', 'منتج')}</strong></div>"""
