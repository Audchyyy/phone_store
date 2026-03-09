from extensions import db
from flask_login import UserMixin

# ตารางสมาชิก
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# ตารางสินค้า (ข้อมูลที่สนใจ)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    # เชื่อมโยงว่าใครเป็นคนเพิ่มข้อมูลนี้
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))