from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from student_management_system_app.models import CustomUser, AdminHOD, Staffs, Students, Courses, Subjects
from student_management_system_app.models import Attendance, AttendanceReport, LeaveReportStaff, LeaveReportStudent, FeedBackStaffs, FeedBackStudent, NotificationStaffs, NotificationStudent


class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)