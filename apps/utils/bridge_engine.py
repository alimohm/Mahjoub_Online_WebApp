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
            response = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=20)
            return response.json()
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")
            return {}

    def fetch_products(self, search_term="", page=1):
        """
        محرك بحث لحظي: يرسل نص البحث مباشرة إلى قمرة.
        """
        # الاستعلام يدعم المتغيرات للبحث والترقيم
        query = """
        query($q: String, $page: Int) {
            findAllProducts(search: $q, page: $page) {
                data {
                    title
                    pricing { price }
                    quantity
                    status
                    images { 
                        fileUrl 
                    }
                }
            }
        }
        """
        variables = {"q": search_term, "page": page}
        result = self.execute_query(query, variables=variables)
        
        products = result.get('data', {}).get('findAllProducts', {}).get('data', [])
        
        processed_products = []
        for p in products:
            pricing = p.get('pricing') or {}
            images = p.get('images') or []
            
            img_url = None
            if isinstance(images, list) and len(images) > 0:
                img_url = images[0].get('fileUrl')
            
            processed_products.append({
                'title': p.get('title'),
                'price': pricing.get('price', 0),
                'quantity': p.get('quantity', 0),
                'status': p.get('status'),
                'image_url': img_url
            })
                
        return processed_products
