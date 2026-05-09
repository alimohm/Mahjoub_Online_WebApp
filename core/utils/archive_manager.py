import os
import requests
import base64
import json # تم استيرادها هنا بشكل ثابت
from datetime import datetime
from flask import current_app

class ArchiveManager:
    def __init__(self):
        # تأكد أن هذا المتغير موجود في إعدادات Railway
        self.token = os.getenv('SOVEREIGN_ASSETS_TOKEN')
        self.repo_owner = "alimohm"
        self.repo_name = "Mahjoub-Sovereign-Assets"
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/"

    def _get_headers(self):
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def generate_path(self, entity_id, folder_name="Registry"): # تغيير الاسم للإنجليزية
        """
        توليد المسار الهرمي بشكل متوافق مع الروابط العالمية
        """
        now = datetime.now()
        # المسار الناتج سيبدو هكذا: 963001/2026/05/09/Registry
        path = f"{entity_id}/{now.year}/{now.month:02d}/{now.day:02d}/{folder_name}"
        return path

    def archive_file(self, file_data, filename, entity_id, folder_name="Registry", commit_type="Archiving"):
        if not self.token:
            print("❌ خطأ سيادي: الـ Token غير موجود في متغيرات البيئة!")
            return False

        # بناء المسار
        target_path = f"{self.generate_path(entity_id, folder_name)}/{filename}"
        url = self.api_url + target_path

        # التشفير
        if hasattr(file_data, 'read'):
            content = file_data.read()
            encoded_content = base64.b64encode(content).decode('utf-8')
        else:
            # إذا كانت البيانات نصاً أو bytes مباشرة
            data_bytes = file_data if isinstance(file_data, bytes) else file_data.encode('utf-8')
            encoded_content = base64.b64encode(data_bytes).decode('utf-8')

        commit_message = f"{commit_type} - ID: {entity_id} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

        payload = {
            "message": commit_message,
            "content": encoded_content
        }

        try:
            response = requests.put(url, json=payload, headers=self._get_headers())
            if response.status_code in [201, 200]:
                print(f"✅ تم الأرشفة بنجاح في المسار: {target_path}")
                return response.json()['content']['download_url']
            else:
                print(f"❌ فشل الرفع. الرد من GitHub: {response.json().get('message')}")
                return False
        except Exception as e:
            print(f"❌ خطأ تقني في المحرك: {str(e)}")
            return False

    def archive_data_as_json(self, data_dict, filename, entity_id, folder_name="Daily_Logs"): # تغيير الاسم للإنجليزية
        """
        أرشفة السجلات الرقمية بصيغة JSON
        """
        json_data = json.dumps(data_dict, indent=4, ensure_ascii=False)
        return self.archive_file(
            json_data, 
            f"{filename}.json", 
            entity_id, 
            folder_name, 
            commit_type="Data Archive"
        )

archive_sys = ArchiveManager()
