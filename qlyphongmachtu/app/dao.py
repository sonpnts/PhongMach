
import hashlib
from app import app,db
from app.models import Patient, Account
import cloudinary.uploader



def get_user_by_id(user_id):
    return Account.query.get(user_id)


def auth_user(email, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Account.query.filter(Account.email.__eq__(email.strip()),
                                Account.password.__eq__(password)).first()


def add_user(name, email, password, err_msg):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Patient(name=name, email=email, password=password)
    db.session.add(u)
    db.session.commit()
    err_msg="Bạn đã đăng ký thành công"


def update_info(namSinh,sdt,diaChi,avatar,Patient_id):
    p = Patient.query.filter_by(id=Patient_id).first()
    if p:
        p.namSinh = namSinh
        p.sdt = sdt
        p.diaChi = diaChi
        if avatar:
            res = cloudinary.uploader.upload(avatar)
            print(res)
            p.avatar = res['secure_url']

        db.session.commit()
