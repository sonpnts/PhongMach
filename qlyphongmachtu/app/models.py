from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app import db
from datetime import datetime
from flask_login import UserMixin
import hashlib


class Account(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    name = Column(String(50), nullable=False)
    avatar = Column(String(255),default="https://cdn-icons-png.flaticon.com/512/3177/3177440.png")

    type = Column(String(50), default="patient")
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __str__(self):
        return self.id

class Doctor(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    ngayVaoLam = Column(String(50), nullable=False)
    medical_forms = relationship('MedicalForm', backref='doctor', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'doctor'
    }

class Admin(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    ngayTao = Column(String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

class Patient(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    diaChi = Column(String(50))
    namSinh = Column(String(50))
    sdt = Column(String(50))
    joined_date = Column(DateTime, default=datetime.now())
    #active = Column(Boolean, default=False)
    books = relationship('Books', cascade="all,delete", backref='patient', lazy=True)
    medical_forms = relationship('MedicalForm', backref='patient', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'patient'
    }

class Nurse(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    phuTrachKhoa = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'nurse'
    }

class Cashier(Account):
    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    chucVu = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'cashier'
    }

class Time(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(String(20), nullable=False)
    books_times = relationship('Books', backref='time', lazy=True)

    def __str__(self):
        return self.period

class Books(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    booked_date = Column(DateTime, default=datetime.now())
    patient_id = Column(Integer, ForeignKey(Patient.id,  onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    time_id = Column(Integer, ForeignKey(Time.id), nullable=False)

    def __str__(self):
        return self.id


class Medicine(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    unit = Column(String(10), nullable=False)
    price = Column(Integer, nullable=False)
    usage = Column(String(100))
    prescription = relationship('Prescription', backref='medicine', lazy=True)

    def __str__(self):
        return self.name

class MedicalForm(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.now())
    description = Column(String(100))
    disease = Column(String(50), nullable=False)
    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    prescription = relationship('Prescription', backref='medicalForm', lazy=True)

    def __str__(self):
        return self.id


class Prescription(db.Model):               #Đơn thuốc
    id = Column(Integer, primary_key=True, autoincrement=True)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    quantity = Column(Integer, default=0)
    medicalForm_id = Column(Integer, ForeignKey(MedicalForm.id), nullable=False)

    def __str__(self):
        return self.id



if __name__ == "__main__":
    from app import app
    with app.app_context():
        db.create_all()

        a = Patient(name='Pham Ngoc Son', email='truongson@gmail.com',
                    password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()))

        d = Doctor(name='Truong Dinh Cuong', email='nhatcuong@gmail.com',
                    password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()), type="doctor", ngayVaoLam="14/11/2022")

        db.session.add(a)
        db.session.add(d)
        db.session.commit()
        #
        # t1 = Time(period='07:00 - 08:00')
        # t2 = Time(period='08:00 - 09:00')
        # t3 = Time(period='09:00 - 10:00')
        # t4 = Time(period='10:00 - 11:00')
        # t5 = Time(period='11:00 - 12:00')
        # t6 = Time(period='13:00 - 14:00')
        # t7 = Time(period='14:00 - 15:00')
        # t8 = Time(period='15:00 - 16:00')
        # t9 = Time(period='16:00 - 17:00')
        # t10 = Time(period='17:00 - 18:00')
        # t11 = Time(period='18:00 - 19:00')
        #
        #
        # db.session.add(t1)
        # db.session.add(t2)
        # db.session.add(t3)
        # db.session.add(t4)
        # db.session.add(t5)
        # db.session.add(t6)
        # db.session.add(t7)
        # db.session.add(t8)
        # db.session.add(t9)
        # db.session.add(t10)
        # db.session.add(t11)
        #
        # db.session.commit()

        # m1 = Medicine(name='Panadol', unit='Vỉ', price=25000, usage='Thuốc giảm đau, hạ sốt')
        # m2 = Medicine(name='Becberin', unit='Lọ', price=20000, usage='Thuốc tiêu hóa')
        # m3 = Medicine(name='Paracetamol', unit='Vỉ', price=30000, usage='Thốc hạ sốt, cảm cúm')
        #
        # db.session.add(m1)
        # db.session.add(m2)
        # db.session.add(m3)
        #
        # db.session.commit()

