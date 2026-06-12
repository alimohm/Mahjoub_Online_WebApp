# coding: utf-8
# 📂 apps/utils/bridge_engine.py - محرك الربط المحدث (Mahjoub Bridge Engine)

import requests
from config import Config

class QumraBridgeEngine:
    def __init__(self):
        self.endpoint = "https://mahjoub.online/admin/graphql"
        # تم تحديث الـ Header ليتوافق مع الممارسات الشائعة في GraphQL
        # إذا استمر خطأ 403، جرب استبدال 'x-api-key' بـ 'Authorization'
        self.headers = {
            "x-api-key": Config.QUMRA_API_KEY.strip(), 
            "Content-Type": "application/json"
        }

    def execute_query(self, query, variables=None):
        payload = {"query": query, "variables": variables or {}}
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Bridge Engine Error: {e}")
            return {"errors": str(e)}

    def fetch_latest_products(self, limit=10, page=1):
        """تحديث الاستعلام ليطابق الهيكلية المكتشفة في الـ Sandbox"""
        query = """
        query GetProducts($limit: Int, $page: Int) {
            findAllProducts(input: { limit: $limit, page: $page }) {
                data {
                    title
                    quantity
                    pricing {
                        price
                    }
                }
            }
        }
        """
        variables = {"limit": limit, "page": page}
        result = self.execute_query(query, variables)
        
        # استخراج البيانات بناءً على الهيكلية الجديدة
        if result and 'data' in result:
            return result['data'].get('findAllProducts', {}).get('data', [])
        return []

    # دالة map_product_to_qumra ستحتاج لتحديث لاحقاً بعد التأكد من عمل الاستعلام (Fetch)
