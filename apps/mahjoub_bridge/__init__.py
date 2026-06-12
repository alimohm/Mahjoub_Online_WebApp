# coding: utf-8
from flask import Blueprint

# تعريف الجسر كـ Blueprint
mahjoub_bridge = Blueprint('mahjoub_bridge', __name__, template_folder='templates')

# سنقوم لاحقاً باستيراد المسارات هنا
from apps.mahjoub_bridge import routes
