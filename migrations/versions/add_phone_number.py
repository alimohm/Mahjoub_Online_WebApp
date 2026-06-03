"""add phone number to admin_users

Revision ID: add_phone_number_2026_06_03
Revises: None
Create Date: 2026-06-03 17:35:00.000000

"""
from alembic import op
import sqlalchemy as sa

# رقم مراجعة الهجرة (هذا المعرف يستخدمه النظام ليتتبع التعديلات)
revision = 'add_phone_number_2026_06_03'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """
    الدالة التي يتم تنفيذها عند ترقية قاعدة البيانات.
    تقوم بإضافة عمود phone_number لجدول admin_users.
    """
    op.add_column('admin_users', sa.Column('phone_number', sa.String(length=20), nullable=False))

def downgrade():
    """
    الدالة التي يتم تنفيذها عند التراجع عن التحديث.
    تقوم بحذف عمود phone_number من جدول admin_users.
    """
    op.drop_column('admin_users', 'phone_number')
