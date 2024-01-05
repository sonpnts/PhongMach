from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db
from app.models import Time, Medicine


admin = Admin(app=app, name="QUẢN TRỊ PHÒNG MẠCH TƯ", template_mode="bootstrap4")


class TimelView(ModelView):
    can_export = True

class MedicinelView(ModelView):
    column_searchable_list = ['name']
    column_filters = ['price', 'name']
    can_export = True
    can_view_details = True

class MyStatsView(BaseView):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')




admin.add_view(TimelView(Time, db.session))
admin.add_view(MedicinelView(Medicine, db.session))
admin.add_view(MyStatsView(name='Thống kê báo cáo'))
