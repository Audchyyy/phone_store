from flask import Flask, render_template, redirect, url_for, request, flash
from extensions import db, login_manager
from models import User, Product
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

app = Flask(__name__)

# 1. การตั้งค่า (Configuration)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://phone_store_db_2hvg_user:uZ7ZucDxAispPh8MFS87c6wfymH4Ul5y@dpg-d6nd075actks738km1h0-a.singapore-postgres.render.com/phone_store_db_2hvg'
app.config['SECRET_KEY'] = 'apple-store-secret-key'

# 2. เริ่มต้นระบบ
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# สร้างตาราง
with app.app_context():
    db.create_all()

# 3. เส้นทาง (Routes)

@app.route("/")
def index():
    return render_template("index.html")

# --- เพิ่มฟังก์ชัน login ที่หายไป ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        userExists = User.query.filter_by(email=email).first()
        if userExists:
            flash('Email already registered!')
            return redirect(url_for('signup'))

        new_user = User(
            username=f"{first_name}_{last_name}",
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# 4. รันโปรแกรม (ต้องอยู่ล่างสุดเสมอ!)
if __name__ == "__main__":
    app.run(debug=True)