from flask import Flask, render_template, redirect, url_for
from extensions import db, login_manager
from models import User, Product

app = Flask(__name__)

# ตั้งค่าฐานข้อมูลจาก Render
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@hostname/dbname'
app.config['SECRET_KEY'] = 'apple-store-secret-key'

# เริ่มต้นระบบ
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# สร้างตารางอัตโนมัติ (เฉพาะครั้งแรกหรือเมื่อมีการเปลี่ยนแปลง)
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)