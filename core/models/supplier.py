import os
import json
import base64
import requests
from datetime import datetime

class ArchiveManager:
    """
    نظام الأرشفة السيادية لترسانة محجوب أونلاين
    المسؤول عن توثيق العمليات ورفعها إلى مستودع GitHub الخاص
    """
    def __init__(self):
        # تم دمج التوكن الذي أرسلته لتأمين الاتصال
        self.github_token = "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"
        self.repo_name = "Mahjoub-Online-Archive" # تأكد من إنشاء هذا المستودع في حسابك
        self.username = "Ali-Mahjoub" # ضع يوزر GitHub الخاص بك هنا
        self.base_url = f"https://api.github.com/repos/{self.username}/{self.repo_name}/contents/"

    def archive_data_as_json(self, data_dict, filename, entity_id, folder_name="Suppliers"):
        """
        أرشفة البيانات بصيغة JSON ورفعها فوراً إلى GitHub
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = f"Archives/{folder_name}/{entity_id}/{filename}_{timestamp}.json"
        
        # تحويل البيانات إلى JSON مشفر بـ Base64 (متطلب GitHub API)
        content = json.dumps(data_dict, indent=4, ensure_ascii=False)
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

        payload = {
            "message": f"Sovereign Archive: {filename} for {entity_id}",
            "content": encoded_content
        }

        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        # تنفيذ عملية الرفع
        response = requests.put(self.base_url + path, headers=headers, json=payload)

        if response.status_code in [201, 200]:
            print(f"✅ تم الأرشفة بنجاح: {path}")
            return True
        else:
            print(f"❌ فشل الأرشفة: {response.json().get('message')}")
            return False

# إنشاء نسخة مفعلة وجاهزة للاستخدام في النظام
archive_sys = ArchiveManager()
