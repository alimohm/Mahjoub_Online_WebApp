from core import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='supplier') # 'admin' or 'supplier'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    supplier_profile = db.relationship('Supplier', backref='user_account', uselist=False)
