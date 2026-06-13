# coding: utf-8
# 📂 apps/utils/bridge_engine.py

import requests
import os

class QumraBridgeEngine:
    def __init__(self):
        self.endpoint = "https://mahjoub.online/admin/graphql"
        api_token = os.environ.get('QUMRA_API_KEY', '').strip()
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def execute_query(self, query, variables=None):
        payload = {"query": query, "variables": variables or {}}
        try:
            response = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=15)
            result = response.json()
            return result
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")
            return {}

    def fetch_latest_products(self):
        # استعلام لكشف الحقول المتاحة في ImageProduct
        introspection_query = """
        query {
            __type(name: "ImageProduct") {
                fields {
                    name
                }
            }
        }
        """
        debug_response = self.execute_query(introspection_query)
        print(f"DEBUG: Schema Discovery Result: {debug_response}")

        # استعلام تجريبي لجلب المنتجات بدون الحقول الفرعية المسببة للخطأ
        query = """
        query {
            findAllProducts {
                data {
                    title
                    pricing { price }
                    quantity
                    status
                    images { url } 
                }
            }
        }
        """
        data_response = self.execute_query(query)
        print(f"DEBUG: Products Query Result: {data_response}")
        
        return []
