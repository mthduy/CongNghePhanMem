from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from saleapp import app,db
from models import Category, Product


admin= Admin(app= app, name="E-commerce Website", template_mode="bootstrap4")

admin.add_views(ModelView(Category,db.session))
admin.add_views(ModelView(Product,db.session))