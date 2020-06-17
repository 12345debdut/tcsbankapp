from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from decouple import config
import os
app=Flask(__name__)
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY') or config('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('SQLALCHEMY_DATABASE_URI') or config('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=bool(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')) or bool(config('SQLALCHEMY_TRACK_MODIFICATIONS'))
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
ma=Marshmallow(app)



from bank import routes