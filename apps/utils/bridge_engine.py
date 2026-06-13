# coding: utf-8
# 📂 apps/utils/bridge_engine.py

import requests
import os
from config import Config

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
            
            if response.status_code != 200:
                print(f"❌ DEBUG: Status {response.status_code} | Body: {response.text}")
                return {}
            
            result = response.json()
            
            if 'errors' in result:
                print(f"❌ GraphQL Errors: {result['errors']}")
                return {}
                
            return result.get('data', {})
            
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")
            return {}

    def fetch_latest_products(self, limit=10):
        # 🔍 استعلام الفحص (Introspection Query) لكشف أسماء الحقول الصحيحة
        query = """
        query {
            __schema {
                queryType {
                    fields {
                        name
                    }
                }
            }
        }
        """
        data = self.execute_query(query)
        print(f"DEBUG: Schema Fields Discovery: {data}")
        
        return []
