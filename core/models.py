import requests
import os
from core.models import db, Product

class QumraSyncManager:
    def __init__(self):
        # هذه المتغيرات سيقرأها من رويال تلقائياً
        self.api_url = "https://mahjoub.online/admin/graphql"
        self.token = os.environ.get("QUMRA_API_KEY")

    def fetch_and_sync(self):
        if not self.token:
            return False, "API Key missing in Railway variables"

        # الاستعلام الذي رأيناه في صور Apollo
        query = """
        query {
          products(first: 10) {
            data {
              _id
              title
              handle
            }
          }
        }
        """
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(self.api_url, json={'query': query}, headers=headers)
            result = response.json()
            
            products_data = result.get('data', {}).get('products', {}).get('data', [])
            
            for p in products_data:
                # التأكد من عدم تكرار المنتج
                existing = Product.query.filter_by(qumra_id=p['_id']).first()
                if not existing:
                    new_product = Product(
                        qumra_id=p['_id'],
                        name=p['title'],
                        handle=p['handle']
                    )
                    db.session.add(new_product)
            
            db.session.commit()
            return True, f"تمت مزامنة {len(products_data)} منتجات بنجاح!"
            
        except Exception as e:
            return False, str(e)

qumra_manager = QumraSyncManager()
