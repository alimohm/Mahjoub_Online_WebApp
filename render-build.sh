#!/usr/bin/env bash
# تحديث وتثبيت مكتبات النظام المطلوبة لـ WeasyPrint
apt-get update
apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libffi-dev shared-mime-info
pip install -r requirements.txt
