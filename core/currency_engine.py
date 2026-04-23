import requests

class CurrencyEngine:
    def __init__(self):
        # أسعار صرف ثابتة كمثال (يمكنك جعلها متغيرة لاحقاً عبر API)
        self.rates = {
            'SAR_TO_YER': 530.0,  # سعر صرف الريال السعودي مقابل اليمني
            'USD_TO_YER': 1600.0, # سعر صرف الدولار مقابل اليمني
            'MARKUP': 0.10        # نسبة ربح المنصة الافتراضية (10%)
        }

    def convert(self, amount, from_currency, to_currency):
        """تحويل المبالغ بين العملات"""
        if from_currency == 'SAR' and to_currency == 'YER':
            return amount * self.rates['SAR_TO_YER']
        # يمكنك إضافة المزيد من شروط التحويل هنا
        return amount

    def calculate_final_price(self, base_price, supplier_markup=0):
        """حساب السعر النهائي للمستهلك شامل عمولة المنصة"""
        platform_fee = base_price * self.rates['MARKUP']
        final_price = base_price + platform_fee + supplier_markup
        return round(final_price, 2)

# نسخة جاهزة للاستخدام في بقية الملفات
currency_engine = CurrencyEngine()
