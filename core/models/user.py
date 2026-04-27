from core import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='supplier')  # 'admin' أو 'supplier'
    
    # ربط المستخدم ببيانات المورد إذا كان دوره مورد
    supplier_profile = db.relationship('Supplier', backref='user', uselist=False)
