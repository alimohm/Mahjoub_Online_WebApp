# coding: utf-8
# 📂 apps/utils/bridge_engine.py - محرك المزامنة السيادي (مطور)

import requests
from config import Config

class QumraBridgeEngine:
    def __init__(self):
        self.endpoint = "https://mahjoub.online/admin/graphql"
        api_token = getattr(Config, 'QUMRA_API_KEY', '') or ""
        self.headers = {
            "Authorization": f"Bearer {api_token.strip()}",
            "Content-Type": "application/json",
            "apollo-require-preflight": "true" 
        }

    def execute_query(self, query, variables=None):
        payload = {"query": query, "variables": variables or {}}
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, dict) else {}
        except Exception as e:
            print(f"⚠️ Bridge Engine Error: {e}")
            return {}

    def fetch_latest_products(self, limit=10, page=1):
        # تم إضافة image_url و description لجلب البيانات كاملة
        query = """
        query GetProducts($limit: Int, $page: Int) {
            findAllProducts(input: { limit: $limit, page: $page }) {
                data {
                    title
                    quantity
                    image_url
                    description
                    pricing {
                        price
                    }
                }
            }
        }
        """
        variables = {"limit": limit, "page": page}
        result = self.execute_query(query, variables)
        
        if not result or 'data' not in result: return []
            
        data_wrapper = result.get('data', {})
        find_all = data_wrapper.get('findAllProducts', {})
        products = find_all.get('data', [])
        
        # إضافة "القالب التلقائي" لكل منتج هنا
        for p in products:
            p['auto_template'] = self.generate_product_html(p)
            
        return products if isinstance(products, list) else []

    def generate_product_html(self, product):
        """توليد قالب HTML مصغر للمنتج تلقائياً عند المزامنة"""
        price = product.get('pricing', {}).get('price', 0)
        img = product.get('image_url') or 'https://via.placeholder.com/200'
        return f"""
        <div class="product-snippet">
            <img src="{img}" style="width:50px; height:50px;">
            <h6>{product.get('title')}</h6>
            <span>السعر: {price} ر.س</span>
        </div>
        """
