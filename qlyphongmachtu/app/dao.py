import hashlib
from datetime import date, datetime

from sqlalchemy import extract, func

from app import app,db
from app.models import Patient, Account, Books, Time, Medicine, MedicalForm, Prescription, Cashier, Receipt, Rules
import cloudinary.uploader
from flask_login import current_user
from twilio.rest import Client



def add_booking(desc, date, time):
    b = Books(desc=desc, booked_date=date, time_id=time,patient=current_user)
    print('acb')
    db.session.add(b)
    db.session.commit()
    return b

def load_booking():
    return Books.query.all()

def load_book():
    return Books.query.all()


def load_time():
    return Time.query.all()

def load_patient():
    return Patient.query.all()


def load_patient(kw=None):
    patients = Patient.query
    if kw:
        patients = patients.filter(Patient.name.contains(kw))

    return patients.all()


def load_cashier():
    return Cashier.query.all()

def load_cash():
    return Cashier.query.all()



def load_medicine(kw=None):
    medicines = Medicine.query
    if kw:
        medicines = medicines.filter(Medicine.name.contains(kw))

    return medicines.all()


def load_medicine():
    return Medicine.query.all()

def load_medicalForm():
    return MedicalForm.query.all()

def load_prescription():
    return Prescription.query.all()



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



def update_info(namSinh,sdt,diaChi,avatar,Patient_id, gioiTinh):
    p = Patient.query.filter_by(id=Patient_id).first()
    a = Account.query.filter_by(id=Patient_id).first()
    if p:
        p.namSinh = namSinh
        p.sdt = sdt
        p.diaChi = diaChi
        p.gioiTinh = gioiTinh
        if avatar:
            res = cloudinary.uploader.upload(avatar)
            print(res)
            a.avatar = res['secure_url']

        db.session.commit()

def lenlichkham(id):
    b = Books.query.filter_by(id=id).first()
    b.lenLichKham = True
    db.session.commit()


def lenphieukham(id):
    b = Books.query.filter_by(id=id).first()
    p = Patient.query.filter_by(id=b.patient_id).first()
    b.isKham = True
    db.session.commit()

    return p


def lenphieukhamxong(id):
    b = Books.query.filter_by(id=id).first()
    b.isKham = True
    db.session.commit()


def book_off(name, sdt, namSinh, diaChi, gioiTinh):
    p = Patient(name=name, sdt=sdt, namSinh=namSinh, diaChi=diaChi, gioiTinh=gioiTinh)
    db.session.add(p)
    db.session.commit()

    return p


def add_book_offline(time, id,desc):
    b = Books(time_id=time,patient_id=id, desc=desc)
    db.session.add(b)
    db.session.commit()



def add_medical_form(id, description, disease):
    mf = MedicalForm(patient_id=id, description=description, disease=disease, date=date.today(), doctor_id=current_user.id)
    db.session.add(mf)
    db.session.commit()

    return mf.id

def add_prescription( medicine, quantity, guide, id):
    me = Medicine.query.filter_by(name=medicine).first()
    pr = Prescription(medicalForm_id=id, medicine_id=me.id, quantity=quantity, guide=guide)
    db.session.add(pr)
    db.session.commit()



def sms(id):
    # b = Books.query.filter_by(id=id).first()
    # account_sid = 'AC190aec1c752f38726ac98a57ed1356b7'
    # auth_token = 'a861de3ac30443372b918a9484c690b0'
    # twilio_number = '+13035005221'
    # my_phone = '+84374202752'
    #
    # client = Client(account_sid, auth_token)
    #
    # result = db.session.query(Books, Time) \
    #     .join(Time, Books.time_id == Time.id).all()
    #
    # for books, time in result:
    #     message_body = (
    #         f"Xin chào bạn, đây là tin nhắn từ Phòng Mạch Tư ABC!\n"
    #         f"Lịch khám của bạn là ngày {books.booked_date} lúc {time.period}\n"
    #         "Địa chỉ: 123 Nguyễn Văn Cừ, Quận 1, TP.HCM\n"
    #         "Lưu ý, bạn vui lòng đến trước 30 phút để làm thủ tục khám bệnh\n"
    #         "Xin cảm ơn!"
    #     )
    #
    # message = client.messages.create(
    #     body=message_body,
    #     from_=twilio_number,
    #     to=my_phone
    # )
    # print(message.sid)
    pass



def lenhoadon(id):
    medical_form = MedicalForm.query.get(id)
    patient = Patient.query.get(medical_form.patient_id)
    return patient.id

def load_examines_price():
    return Rules.query.filter_by(name='tienkham').first().value

def load_quantity_patient():
    return Rules.query.filter_by(name='quantity_patient').first().value


def add_receipt(patient_id, examines_price, total):
    r = Receipt(created_date=datetime.now().date(),cashier_id=current_user.id,patient_id=patient_id
                ,examines_price=examines_price,total_price=total)
    db.session.add(r)
    db.session.commit()



def su_dung_thuoc(month):
    with app.app_context():
        # Tạo truy vấn cơ bản
        query = db.session.query(
            Medicine.name,
            extract('month', MedicalForm.date).label('Tháng'),
            (func.sum(Prescription.quantity) / 30 * 100).label('Tần suất sử dụng')
        )\
        .join(Prescription, Prescription.medicine_id == Medicine.id)\
        .join(MedicalForm, MedicalForm.id == Prescription.medicalForm_id)\
        .group_by(Medicine.name, extract('month', MedicalForm.date))

        results = query.all()

        return results



def tan_suat_kham(month):
    with app.app_context():
        query = db.session.query(
            extract('month', MedicalForm.date).label('Tháng'),
            (func.count(MedicalForm.id) / 30*100).label('Tần suất khám')
        ).group_by(extract('month', MedicalForm.date))


        results = query.all()

        return results






def doanh_thu_thang(month):
    with app.app_context():
        query = db.session.query(
            extract('month', Receipt.created_date).label('Tháng'),
            func.sum(Receipt.total_price).label('Doanh thu')
        ).group_by(extract('month', Receipt.created_date))

        results = query.all()

        return results
