from flask import Flask, render_template, redirect, url_for, request, flash
from extensions import db, login_manager
from models import User, Product
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

app = Flask(__name__)

# 1. การตั้งค่า
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://phone_store_db_2hvg_user:uZ7ZucDxAispPh8MFS87c6wfymH4Ul5y@dpg-d6nd075actks738km1h0-a.singapore-postgres.render.com/phone_store_db_2hvg'
app.config['SECRET_KEY'] = 'apple-store-secret-key'

# 2. เริ่มต้นระบบ
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

login_manager.login_view = 'login'

# สร้างตาราง
with app.app_context():
    db.create_all()

# ─────────────────────────────────────────
# หน้าหลัก
# ─────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ─────────────────────────────────────────
# Auth: Login / Signup / Logout
# ─────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        user     = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('อีเมลหรือรหัสผ่านไม่ถูกต้อง')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email      = request.form.get('email')
        password   = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name  = request.form.get('last_name')

        if User.query.filter_by(email=email).first():
            flash('อีเมลนี้ถูกใช้งานแล้ว')
            return redirect(url_for('signup'))

        new_user = User(
            username=f"{first_name} {last_name}",
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ─────────────────────────────────────────
# Products: แสดง + CRUD
# ─────────────────────────────────────────

# ✅ ไม่มี @login_required → ทุกคนเห็นสินค้าได้
@app.route('/products')
def products():
    q = request.args.get('q', '')
    if q:
        product_list = Product.query.filter(Product.name.ilike(f'%{q}%')).all()
    else:
        product_list = Product.query.all()
    return render_template('products/index.html', products=product_list, q=q)


# ✅ @login_required → เฉพาะคนที่ login เท่านั้น
@app.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name        = request.form.get('name')
        description = request.form.get('description')
        price       = request.form.get('price')

        new_product = Product(
            name=name,
            description=description,
            price=float(price),
            user_id=current_user.id
        )
        db.session.add(new_product)
        db.session.commit()
        flash('เพิ่มสินค้าสำเร็จ!')
        return redirect(url_for('products'))  # ✅ แก้จาก admin_products

    return render_template('products/add.html')


@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name        = request.form.get('name')
        product.description = request.form.get('description')
        product.price       = float(request.form.get('price'))
        db.session.commit()
        flash('แก้ไขสินค้าสำเร็จ!')
        return redirect(url_for('products'))  # ✅ แก้จาก admin_products

    return render_template('products/edit.html', product=product)


@app.route('/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('ลบสินค้าสำเร็จ!')
    return redirect(url_for('products'))  # ✅ แก้จาก admin_products


# 4. รันโปรแกรม
if __name__ == "__main__":
    app.run(debug=True)