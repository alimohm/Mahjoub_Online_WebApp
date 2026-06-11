# 📂 apps/models/settlements_db.py
from apps.extensions import db
from datetime import datetime
import uuid

class AdminSettlement(db.Model):
    __tablename__ = 'admin_settlements'
    
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=False)
    wallet_code = db.Column(db.String(50))
    settlement_code = db.Column(db.String(20), unique=True)
    amount = db.Column(db.Numeric(15, 2))
    status = db.Column(db.String(20), default='منفذة')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def generate_settlement_code():
        return f"SET-{uuid.uuid4().hex[:8].upper()}"
