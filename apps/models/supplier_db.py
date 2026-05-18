# coding: utf-8
# 🔑 مستند النموذج الحوكمي للموردين - منصة محجوب أونلاين 2026

from apps import db
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.orm import validates, object_session  # استيراد أدوات التحقق والجلسات الذكية

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    # 1. المعرفات الأساسية
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column(db.String(50), unique=True, nullable=False, index=True) # المعرف الموحد السيادي المؤرشف
    
    # [الحقل 1] اسم المستخدم - فريد وإجباري
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # 2. بيانات التوثيق
    identity_type = db.Column(db.String(50), nullable=False)    # نوع الهوية (جعلناه إجباري)
    
    # [الحقل 2] رقم الوثيقة / الهوية - تم تعميده فريد وإجباري لمنع التكرار
    identity_number = db.Column(db.String(50), unique=True, nullable=False)  
    identity_image = db.Column(db.String(255))   # مسار صورة الهوية
    
    # 3. بيانات المالك والمنشأة
    # [الحقل 3] اسم المالك الكامل - تم تعميده فريد وإجباري
    owner_name = db.Column(db.String(150), unique=True, nullable=False)
    
    # [الحقل 4] هاتف المالك الشخصي - تم تعميده فريد وإجباري
    owner_phone = db.Column(db.String(20), unique=True, nullable=False)       
    
    # [الحقل 5] الاسم التجاري للمنشأة - فريد وإجباري
    trade_name = db.Column(db.String(150), unique=True, nullable=False)
    
    # [الحقل 6] هاتف المنشأة (محل) - تم تعميده فريد وإجباري
    shop_phone = db.Column(db.String(20), unique=True, nullable=False)
    
    activity_type = db.Column(db.String(50))     # فئة المورد
    
    # 4. البيانات الجغرافية
    province = db.Column(db.String(50))
    district = db.Column(db.String(50))
    address_detail = db.Column(db.Text)
    
    # 5. البيانات المالية
    fin_type = db.Column(db.String(20))          # بنوك أم شركات
    bank_name = db.Column(db.String(100))        # اسم الجهة
    
    # [الحقل 7] رقم الحساب المالي - تم تعميده فريد وإجباري لمنع تداخل المستحقات
    bank_acc = db.Column(db.String(50), unique=True, nullable=False)          
    
    # 6. حقول التحكم بالحالة والرتبة (Core Governance Fields)
    status = db.Column(db.String(20), nullable=False, default='pending') 
    # الحالة العامة تقبل برمجياً: 'active' (نشط فوري)، 'pending' (مراجعة)، 'suspended' (معلق/موقوف)
    
    rank_grade = db.Column(db.String(20), nullable=False, default='ريادي') 
    # الهرمية الفخمة المعتمدة: 'ريادي' (المستوى 1)، 'سيادي' (المستوى 2)، 'ملكي' (المستوى الأعلى)

    # 7. حقول الحوكمة وتتبع نظام الصلاحيات
    registration_source = db.Column(db.String(30), nullable=False, default='الموقع الخارجي') 
    # يحدد مكان ولادة الحساب: 'لوحة التحكم' أو 'الموقع الخارجي'
    
    created_by_id = db.Column(db.Integer, nullable=True)  
    updated_by_id = db.Column(db.Integer, nullable=True)  

    # 8. التوثيق والتحليل الزمني (Timestamps)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 

    # =========================================================================
    # 👑 قاموس الترجَمة السيادية للحالات اللفظية الفخمة بناءً على مستويات النفوذ
    # =========================================================================
    @property
    def state_title(self):
        """
        خاصية ذكية ومحصنة تقوم بقراءة حالة النظام ورتبته لتنتج 
        اللقب اللفظي الفخم المخصص للتاجر في واجهة العرض تلقائياً.
        """
        sovereign_matrix = {
            'ريادي': {
                'active': 'مُطلق',
                'pending': 'مراجعة',
                'suspended': 'محتجز'
            },
            'سيادي': {
                'active': 'نافذ / مُهيمِن',
                'pending': 'مراجعة الصلاحية',
                'suspended': 'مُقيد / مجمد السيادة'
            },
            'ملكي': {
                'active': 'حَصين',
                'pending': 'مستقر / صيانة خاصة',
                'suspended': 'معلق الحصانة'
            }
        }
        current_rank_dict = sovereign_matrix.get(self.rank_grade, sovereign_matrix['ريادي'])
        return current_rank_dict.get(self.status, 'تحت التدقيق السيادي')

    # -------------------------------------------------------------------------
    # 🛡️ مصيدة الحوكمة (Validators): منع تمرير المسافات أو القِيَم الفارغة نهائياً
    # -------------------------------------------------------------------------
    @validates('username', 'identity_number', 'owner_name', 'owner_phone', 'trade_name', 'shop_phone', 'bank_acc')
    def validate_sovereign_fields(self, key, value):
        clean_value = str(value).strip() if value is not None else ""
        if not clean_value:
            raise ValueError(f"خطأ حوكمي صارم: الحقل السيادي ({key}) لا يمكن أن يكون فارغاً أو يحتوي على مسافات فقط.")
        return clean_value

    def to_dict(self):
        """تحويل البيانات إلى كود جيسون جاهز لإرساله لواجهات العرض والمودال"""
        serial_num = self.sovereign_id.split('MAH963')[-1] if self.sovereign_id and 'MAH963' in self.sovereign_id else str(self.id)
        
        return {
            "id": self.id,
            "sovereign_id": self.sovereign_id,                            # المعرف السيادي الأساسي: SUP-MAH9631
            "wallet_code": f"WEL-MAH963{serial_num}",                      # كود المحفظة المالي المستنتج والموحد: WEL-MAH9631
            "username": self.username,
            "owner_name": self.owner_name,
            "trade_name": self.trade_name,
            "shop_phone": self.shop_phone,
            "rank_grade": self.rank_grade,
            "status": self.status,
            "state_title": self.state_title  
        }

    def __repr__(self):
        return f'<Supplier {self.sovereign_id} - {self.trade_name}>'


# -------------------------------------------------------------------------
# 🛡️ نظام الحوكمة التلقائي الآمن: توليد المعرف السيادي الموحد قبل الحفظ في القاعدة
# -------------------------------------------------------------------------
def auto_generate_sovereign_id(mapper, connection, target):
    """
    دالة مراقبة (Event Listener) مستقرة ومحمية، تستعين بـ Session الكائن نفسه
    لمنع حدوث تعليق (Deadlock) في قواعد بيانات جيت هاب / ريلواي الحية.
    """
    session = object_session(target)
    if session is None:
        # كحماية احتياطية في حال تعذر جلب الجلسة الحالية
        target.sovereign_id = "SUP-MAH9631"
        return

    # الاستعلام الآمن من خلال الجلسة النشطة الحالية
    last_supplier = session.query(Supplier).order_by(Supplier.id.desc()).first()
    
    if last_supplier and last_supplier.sovereign_id:
        try:
            parts = last_supplier.sovereign_id.split('MAH963')
            last_num = int(parts[-1])
            next_num = last_num + 1
        except (ValueError, IndexError):
            next_num = (last_supplier.id or 0) + 1
    else:
        next_num = 1

    # استبدال القيمة المبدئية المعطاة بالرقم التسلسلي الدقيق والنهائي
    target.sovereign_id = f"SUP-MAH963{next_num}"


# ربط الدالة بحدث "قبل الإدخال" لجدول الموردين بشكل رسمي صارم
event.listen(Supplier, 'before_insert', auto_generate_sovereign_id)
