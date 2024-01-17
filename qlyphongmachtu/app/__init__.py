import cloudinary
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager


app = Flask(__name__)

app.secret_key = '@#$%^&#@$%^$%^&*@#$%^&43567*#$%^&*'

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://sonpnts:%s@localhost/phongmach?charset=utf8mb4' % quote('Son1010@')
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/qlpmt_db?charset=utf8mb4' % quote('Nhatcuong123@')
#app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/qlpmt_db?charset=utf8mb4' % quote('Admin@123')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

cloudinary.config(
    cloud_name="dqec4llav",
    api_key="752187729553174",
    api_secret="LPw7aj9WseIgRmVct7bdppxfa5g"
)



db = SQLAlchemy(app=app)
login = LoginManager(app=app)
