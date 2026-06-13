# coding: utf-8
# 📂 apps/utils/bridge_engine.py

import requests
from config import Config

class QumraBridgeEngine:
    def __init__(self):
        self.endpoint = "https://mahjoub.online/admin/graphql"
        # قراءة المفتاح من الإعدادات
        api_token = getattr(Config, 'QUMRA_API_KEY', '').strip()
        
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def execute_query(self, query, variables=None):
        payload = {"query": query, "variables": variables or {}}
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=15)
            # للتشخيص في حالة عدم جلب بيانات
            if response.status_code != 200:
                print(f"DEBUG: Status {response.status_code} | Body: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            return result.get('data', {})
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")
            return {}

    def fetch_latest_products(self, limit=10):
        # استعلام متوافق مع هيكلية السيرفر المكتشفة
        query = """
        query GetProducts($first: Int) {
            products(first: $first) {
                data {
                    title
                    _id
                }
            }
        }
        """
        variables = {"first": limit}
        data = self.execute_query(query, variables)
        
        # استخراج البيانات من المسار المكتشف
        return data.get('products', {}).get('data', [])
