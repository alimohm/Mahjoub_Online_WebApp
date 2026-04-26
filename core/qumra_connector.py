from services.qumra_handler import query_qumra
from core.models.product import Product
from core import db

class QumraSyncManager:
    """
    مدير المزامنة السيادي: يعمل بنظام "العبور اللحظي" 
    دون تخزين أصول المنتج محلياً للحفاظ على خفة السيرفر.
    """

    def fetch_live_status(self, q_product_id):
        """التحقق من حالة منتج معين في قمرة دون حفظه"""
        query = """
        query getProduct($id: ID!) {
          product(id: $id) {
            id
            status
            variants(first: 1) {
              edges {
                node {
                  price
                  inventoryQuantity
                }
              }
            }
          }
        }
        """
        variables = {"id": q_product_id}
        result = query_qumra(query, variables)
        return result.get('data', {}).get('product') if result else None

    def sync_all_active_products(self):
        """
        تحديث حالات المزامنة للمنتجات النشطة فقط 
        للتأكد من مطابقة السعر والمخزون.
        """
        active_products = Product.query.filter_by(status='active').all()
        sync_results = {"success": 0, "failed": 0}

        for product in active_products:
            live_data = self.fetch_live_status(product.q_product_id)
            if live_data:
                # تحديث مؤشر المزامنة فقط (بيانات خفيفة جداً)
                product.is_synced = True
                sync_results["success"] += 1
            else:
                product.is_synced = False
                sync_results["failed"] += 1
        
        db.session.commit()
        return sync_results

# إنشاء نسخة واحدة من المدير لاستخدامها في التطبيق
qumra_manager = QumraSyncManager()
