import math

from flask_login import login_user,current_user, logout_user
from flask import render_template, request, redirect
import dao
from saleapp import app ,admin,login


@app.route('/')
def index():

    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    page = request.args.get("page")
    products = dao.load_products(q=q, cate_id=cate_id, page=page)
    pages = dao.count_product()
    return render_template('index.html', products=products, pages=math.ceil(pages/app.config["PAGE_SIZE"]))


@app.route('/products/<int:id>')
def details(id):
    product = dao.load_product_by_id(id)
    return render_template('product-details.html', product = product)

@app.route('/register', methods =['get','post'])
def register_user():
    err_msg= None
    if request.method.__eq__('POST'):
        password= request.form.get('password')
        confirm = request.form.get('confirm')
        if password.__eq__(confirm):
            pass
        else:
            err_msg= "Mật khẩu không khớp!!"
    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if current_user.is_authenticated:
        return redirect("/")
    err_msg = None
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)
            return redirect('/')
        else:
            err_msg = "Tài khoản hoặc mật khẩu không đúng!"

    return render_template('login.html', err_msg=err_msg)

@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')

@app.context_processor
def common_attributes():
    return {
        "categories": dao.load_categories()
    }

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)