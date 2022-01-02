from flask import Flask,render_template
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app=Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='raggioconivalli@gmail.com'
app.config['MAIL_PASSWORD']='password'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']="25e7e38c7b8b5455ffe0b4d4"
db=SQLAlchemy(app)
mail=Mail(app)
bcrypt = Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="login_page"
login_manager.login_message_category="info"
engine = create_engine('sqlite:///database.db', echo = True)
meta = MetaData()

conn = engine.connect()

from flaskr import routes