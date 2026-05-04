from django.db import models
from django.conf import settings

class Supplier(models.Model):
    # الربط مع نظام المستخدمين الأساسي
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='supplier_profile'
    )
    
    # المعرفات السيادية (نظام الترسانة)
    sovereign_id = models.CharField(max_length=20, unique=True, verbose_name="المعرف السيادي")
    e_wallet = models.CharField(max_length=50, unique=True, verbose_name="المحفظة الإلكترونية")
    
    # بيانات النشاط والتوثيق
    trade_name = models.CharField(max_length=255, verbose_name="الاسم التجاري")
    owner_name = models.CharField(max_length=255, verbose_name="اسم المالك")
    activity_type = models.CharField(max_length=100, verbose_name="نوع النشاط")
    
    # بيانات الهوية
    id_type = models.CharField(max_length=50, verbose_name="نوع الوثيقة")
    id_card_number = models.CharField(max_length=100, verbose_name="رقم الوثيقة")
    id_image = models.ImageField(upload_to='suppliers/ids/', null=True, blank=True, verbose_name="أرشفة الهوية")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    
    # النطاق الجغرافي (الربط مع Aden, Al-Khokha, Mocha, Hays)
    province = models.CharField(max_length=100, verbose_name="المحافظة")
    district = models.CharField(max_length=100, verbose_name="المديرية")
    address_detail = models.TextField(verbose_name="العنوان التفصيلي")
    
    # الربط المالي السيادي
    FINANCE_TYPES = (
        ('banks', 'بنوك إسلامية'),
        ('exchange', 'شركات صرافة'),
    )
    fin_type = models.CharField(max_length=20, choices=FINANCE_TYPES, default='banks', verbose_name="نوع الربط المالي")
    bank_name = models.CharField(max_length=150, verbose_name="جهة الاستلام")
    bank_acc = models.CharField(max_length=100, verbose_name="رقم الحساب/الآيبان")
    
    # بيانات النظام
    is_active = models.BooleanField(default=True, verbose_name="حالة التعميد")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "مورد سيادي"
        verbose_name_plural = "الموردون المعتمدون"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.trade_name} ({self.sovereign_id})"
