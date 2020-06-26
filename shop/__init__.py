from flask import Flask
## Flask Email ##
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import os
# import pdfkit
from flask_msearch import Search
from flask_login import LoginManager 
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MyShop.db'
app.config['SECRET_KEY']='hfouewhfoiwefoquw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
## MAIL
app.config['DEBUG'] = True
app.config ['MAIL_SERVER'] = 'smtp.office365.com'
app.config ['MAIL_PORT'] = 587
app.config ['MAIL_USE_TLS'] = True
app.config ['MAIL_USE_SSL'] = False
app.config ['MAIL_USERNAME'] = 'reggie1997@hotmail.co.uk'
app.config ['MAIL_PASSWORD'] = ''
app.config ['MAIL_DEFAULT_SENDER'] = 'reggie1997@hotmail.co.uk'
app.config ['MAIL_MAX_EMAILS'] = None
app.config ['MAIL_ASCII_ATTACHMENTS'] = False
# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
 

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB 


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)

migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = u"Please login first"


from shop.products import routes
from shop.admin import routes
from shop.carts import carts
from shop.customers import routes
# Werkzeug==0.15.6