# 📂 apps/utils/whatsapp/message_builder.py
from .api_client import WhatsAppClient

client = WhatsAppClient()

def send_otp_to_admin(phone_number, otp_code):
    # هنا نستدعي قالب واتساب مخصص تم تجهيزه مسبقاً في ميتا باسم 'otp_login'
    # ملاحظة: سنحتاج لاحقاً لربط المتغيرات (مثل الكود) داخل القالب
    return client.send_message(phone_number, "otp_login")
