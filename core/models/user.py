from core import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    # الحقلين معاً لضمان عدم حدوث NotNullViolation
    password = db.Column(db.String(255), nullable=True) 
    password_hash = db.Column(db.String(255), nullable=False)
    
    role = db.Column(db.String(20), nullable=False, default='admin')
    is_active_account = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        hashed = generate_password_hash(password)
        self.password_hash = hashed
        self.password = hashed 

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
