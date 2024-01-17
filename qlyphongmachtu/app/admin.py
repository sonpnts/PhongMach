from datetime import date
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db, dao
from app.models import Time, Medicine, Books, Cashier, Patient, MedicalForm, Doctor, Prescription, Receipt, ReceiptDetails, Rules, Administrator, Nurse
from flask_login import logout_user, current_user
from flask import redirect, request, jsonify
from app import utils


admin = Admin(app=app, name="QUẢN TRỊ PHÒNG MẠCH TƯ", template_mode="bootstrap4")




# class MyAdmin(MyAdminIndexView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/index.html')


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'administrator'

class AuthenticatedAdmin2(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'administrator'

class AuthenticatedDoctor(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'doctor'

class AuthenticatedPatient(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'patient'

class AuthenticatedNurse(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'nurse'

class AuthenticatedCashier(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'cashier'


class AuthenticatedCashierBV(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.type == 'cashier'




class MedicineView(AuthenticatedAdmin):
    column_searchable_list = ['name']
    column_filters = ['price', 'name']
    can_export = True
    can_view_details = True

class MedicineView(AuthenticatedDoctor):
    column_searchable_list = ['name']
    column_filters = ['price', 'name']
    can_export = True
    can_view_details = True

class MedicalFormView(AuthenticatedDoctor):
    column_list = ['patient_id', 'patient', 'description', 'disease', 'date', 'doctor']
    column_searchable_list = ['patient_id']


class PrescriptionView(AuthenticatedDoctor):
    column_list = ['id', 'medicalForm', 'medicalForm.date', 'medicine', 'quantity', 'guide']


class BooksView(AuthenticatedNurse):                     #DS khám bệnh
    can_export = True
    column_list = ['id', 'patient', 'booked_date', 'time']

class PatientView(AuthenticatedNurse):
    can_export = True
    column_list = ['name', 'gioiTinh', 'namSinh', 'diaChi']
    column_filters = ['gioiTinh', 'namSinh']
    column_searchable_list = ['name']


class TimeView(AuthenticatedAdmin):
    can_export = True

class DoctorView(AuthenticatedAdmin):
    column_list = ['name', 'ngayVaoLam']
    column_searchable_list = ['name']
    can_export = True

class NurseView(AuthenticatedAdmin):
    column_list = ['name']
    can_export = True

class CashierView(AuthenticatedAdmin):
    column_list = ['name']

class RulesView(AuthenticatedAdmin):
    column_list = ['administrator', 'change_date', 'name', 'value']

class AdminView(AuthenticatedAdmin):
    column_list = ['name', 'joined_date']

# class MyStatsView(AuthenticatedAdmin2):
#     @expose("/")
#     def index(self):
#         return self.render('admin/stats.html')

class MyLogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class MyStatsView(AuthenticatedAdmin2):
    @expose('/')
    def index(self):
        month = request.args.get('month')

        return self.render('admin/stats.html',
                           doanhthu=dao.doanh_thu_thang(month=month))


class TanSuatKham(AuthenticatedAdmin2):
    @expose('/')
    def index(self):
        month = request.args.get('month')

        return self.render('admin/tansuatkham.html',
                           tanSuatKham=dao.tan_suat_kham(month=month))



class TanSuatThuoc(AuthenticatedAdmin2):
    @expose('/')
    def index(self):
        month = request.args.get('month')

        return self.render('admin/sudungthuoc.html',
                           tanSuatThuoc=dao.su_dung_thuoc(month=month))


admin.add_view(TimeView(Time, db.session))
admin.add_view(MedicineView(Medicine, db.session))

admin.add_view(BooksView(Books, db.session))
admin.add_view(PatientView(Patient, db.session))


admin.add_view(MedicalFormView(MedicalForm, db.session))
admin.add_view(PrescriptionView(Prescription, db.session))


# admin.add_view(ReceiptDetailsView(ReceiptDetails,  db.session,name="Receipt Details", category="Receipt"))
# admin.add_view(PaymentView(name='Lập hóa đơn'))


admin.add_view(DoctorView(Doctor, db.session))
admin.add_view(NurseView(Nurse, db.session))
admin.add_view(CashierView(Cashier, db.session))
admin.add_view(RulesView(Rules, db.session))
admin.add_view(AdminView(Administrator, db.session))



admin.add_view(MyStatsView(name='Thống kê báo cáo'))
admin.add_view(TanSuatKham(name='Thống kê báo cáo theo tần suất khám'))
admin.add_view(TanSuatThuoc(name='Thống kê báo cáo sử dụng thuốc'))
admin.add_view(MyLogoutView(name='Đăng xuất'))