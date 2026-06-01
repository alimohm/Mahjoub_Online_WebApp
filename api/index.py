import sys
import os

# هذا السطر يجبر بايثون على رؤية المجلد الرئيسي للمشروع
sys.path.append(os.getcwd())

from run import app
