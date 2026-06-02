@echo off
cd /d "%~dp0"
git add .
git commit -m "تحديث ملفات المنصة"
git push
echo تم الرفع بنجاح!
pause
