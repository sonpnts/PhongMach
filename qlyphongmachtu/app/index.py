from datetime import date
from flask import Flask, render_template, request, redirect, jsonify
from flask import request
from sqlalchemy import Float

from app import dao, login, utils
from app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Books, MedicalForm, Prescription


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin/login', methods=['post'])
def login_admin_process():
    email = request.form.get('email')
    password = request.form.get('password')

    user = dao.auth_user(email=email, password=password)
    if user:
        login_user(user=user)
        if current_user.type == 'patient':
            return redirect("/")
        elif current_user.type == 'doctor':
            return redirect('/patient-list')
        elif current_user.type == 'nurse':
            return redirect('/nurse')
        elif current_user.type == 'cashier':
            return redirect('/phieukham-list')
        else:
            return redirect('/admin')

    return render_template("login.html")



@app.route('/booking-form')
def booking():
    time = dao.load_time()
    return render_template('booking-form.html', time=time)


@app.route('/api/booking-form', methods=['post'])
@login_required
def add_booking():
    data = request.json
    desc = data.get('desc')
    date = data.get('date')
    time = data.get('time_id')
    print(time)
    try:
        b = dao.add_booking(desc=desc, date=date, time=time)
        print(time)
        print('KHONG LOI')
    except  Exception as e:
        print(str(e))
        return {'status': 404, 'err_msg': 'Chương trình đang bị lỗi'}

    return {'status': 201, 'booking': {
        'id': b.id,
        'desc': b.desc,
        'date': b.booked_date,
        'time_id': b.time_id
    }
            }





@app.route("/login", methods=['get', 'post'])
def login_user_process():
    if request.method.__eq__('POST'):
        email = request.form.get('email')
        password = request.form.get('password')
        user = dao.auth_user(email=email, password=password)
        if user:
            login_user(user=user)
            if current_user.type == 'patient':
                return redirect("/")
            elif current_user.type == 'doctor':
                return redirect('/patient-list')
            elif current_user.type == 'nurse':
                return redirect('/nurse')
            elif current_user.type == 'cashier':
                return redirect('/phieukham-list')
            else:
                return redirect('/admin')

    return render_template("login.html")


@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/logout')
def process_logout_user():
    logout_user()
    return redirect("/login")






@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = ""
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             email=request.form.get('email'),
                             password=password, err_msg=err_msg)
            except:
                err_msg = 'Hệ thống đang bận, vui lòng thử lại sau!'
            else:
                return redirect('/login')
        else:
            err_msg = "Mật khẩu không khớp! Vui lòng nhập lại"
    return render_template('register.html', err_msg=err_msg)


@app.route('/info', methods=['get', 'post'])
def update():
    err_msg = ""

    if request.method.__eq__('POST'):
        try:
            dao.update_info(namSinh=request.form.get('namSinh'),
                            sdt=request.form.get('sdt'),
                            diaChi=request.form.get('diaChi'),
                            avatar=request.files.get('avatar'),
                            gioiTinh=request.form.get('gioiTinh'),
                            Patient_id=current_user.id)
        except:
            err_msg = 'Hệ thống đang bận, vui lòng thử lại sau!'
        else:
            err_msg = "Cập nhật thành công"
        return redirect('/info')
    return render_template('info.html', err_msg=err_msg)


@app.route('/nurse')
@login_required
def nurse():
    books = dao.load_booking()
    patient = dao.load_patient()
    return render_template('nurse.html', books=books, patient=patient, date=date.today())


@app.route('/api/check-patient-count')
def check_patient_count():
    patients_today = Books.query.filter_by(booked_date=date.today()).filter_by(lenLichKham=True).count()
    quantity_patient = dao.load_quantity_patient()
    return jsonify({'patients_today': patients_today,
                    'quantity_patient': quantity_patient,
                    })


@app.route('/len-ds', methods=['post'])
def len_ds():
    data = request.json
    id = str(data.get('id'))
    dao.sms(id)
    dao.lenlichkham(id)
    return jsonify({"message": "Đã lên lịch khám cho bệnh nhân"})


@app.route('/patient-list')
@login_required
def patient_list():
    books = dao.load_book()
    patient = dao.load_patient()
    return render_template('patient-list.html', books=books, patient=patient, date=date.today())


@app.route('/books/<id>', methods=['get', 'post'])
@login_required
def phieukham(id):
    return render_template('phieukham.html', p=dao.lenphieukham(id), medicine=dao.load_medicine())


@app.route('/books', methods=['get', 'post'])
def phieukhamabc():
    if request.method.__eq__('POST'):
        patient_id = request.form.get('p_id'),
        description = request.form.get('description')
        disease = request.form.get('disease')
        medicine = request.form.get('medicine')
        quantity = request.form.get('quantity')
        guide = request.form.get('guide')
        try:
           mf = dao.add_medical_form(patient_id, description, disease)
           dao.add_prescription(medicine, quantity, guide, mf)
        except:
            err_msg = 'Hệ thống đang bận, vui lòng thử lại sau!'
        else:
            err_msg = "Cập nhật thành công"
            return redirect('/patient-list')
    return render_template('phieukham.html', p=patient_id, medicine=dao.load_medicine())


@app.route('/len-pk', methods=['post'])
def len_pk():
    return render_template('phieukham.html')


@app.route('/book-offline', methods=['get', 'post'])
def book_offline():
    if request.method.__eq__('POST'):
        time = request.form.get('timeId')
        try:
            p = dao.book_off(name=request.form.get('name'),
                             sdt=request.form.get('sdt'),
                             namSinh=request.form.get('namSinh'),
                             gioiTinh=request.form.get('gioiTinh'),
                             diaChi=request.form.get('diaChi'), )

            dao.add_book_offline(time=int(time), desc=request.form.get('desc'), id=p.id)
        except:
            err_msg = 'Hệ thống đang bận, vui lòng thử lại sau!'
        else:
            err_msg = "Cập nhật thành công"
            return redirect('/nurse')

    return render_template('book-offline.html', time=dao.load_time())

@app.route('/phieukham-list')
def medicalform_list():
    lapphieukham = utils.get_info_medical_form()
    return render_template('phieukham-list.html', lapphieukham=lapphieukham, tienkham=dao.load_examines_price())



@app.route('/receipt-details')
@login_required
def ReceiptDetailsView():
    receipt_details = utils.get_receipt_details()
    return render_template('receipt-details.html', receipt_details=receipt_details)


# @app.route('/MedicalForm/<id>', methods=['get', 'post'])
# def CreateReceipt(id):
#     print(id)
#     tienkham = dao.load_examines_price()
#     lapphieukham = utils.get_info_medical_form()
#     p = dao.lenhoadon(id)
#     int(p)
#     return render_template('create-receipt.html', p=p
#                            , lapphieukham=lapphieukham, tienkham=tienkham)

#
# @app.route('/create-receipt', methods=['get', 'post'])
# def Payment():
#     if request.method.__eq__('POST'):
#         # medicine_name = request.form.get('medicine_name')
#         medicine_price = request.form.get('medicine_price')
#         total = request.form.get('total')
#         patient_id = request.form.get('patient_id')
#         try:
#             dao.add_receipt(patient_id=patient_id,medicine_price=medicine_price,total=total)
#         except:
#             err_msg = "Lỗi"
#         else:
#             err_msg = "Thanh toán thành công"
#     return render_template(template_name_or_list='receipt_list.html')

# @app.route('/api/receipt-form', methods=['post'])
# def Payment():
#     data = request.json
#     examines_price = data.get('examines_price')
#     total = data.get('total')
#     patient_id = data.get('patient_id')
#     try:
#         examines_price = Float(examines_price)
#         total = Float(total)
#     except (ValueError, TypeError):
#         examines_price = None
#         total = None
#     try:
#         b = dao.add_receipt(patient_id=patient_id, examines_price=examines_price, total=total)
#     except  Exception as e:
#         print(str(e))
#         return {'status': 404, 'err_msg': 'Chương trình đang bị lỗi'}
#
#     return {'status': 201, 'receipt': {
#         'patient_id': b.patient_id,
#         'examines_price': b.examines_price,
#         'total': b.total
#         }
#     }


@app.route('/api/thanhtoan', methods=['POST'])
def Payment():
    data = request.json
    tienThuoc = data.get('tienThuoc')
    tongTien = data.get('tongTien')
    p_id = data.get('id')

    dao.add_receipt(patient_id=p_id, examines_price=tienThuoc, total=tongTien)

    return jsonify({'status': "Cập nhật thành công"})


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
