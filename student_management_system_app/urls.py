from django.urls import path

from student_management_system_app.views import show_demo_page, show_login_page, do_login, get_user_details, \
    logout_user, admin_home, add_staff, add_courses
from student_management_system_app.views import add_staff_save, add_courses_save, add_students, add_students_save

urlpatterns = [
    path("", show_login_page, name="login_page"),
    path("demo", show_demo_page, name="demo"),
    path("doLogin", do_login, name="doLogin"),
    path("get_user_details", get_user_details, name='get_user_details'),
    path("logout_user", logout_user, name='logout'),
    path('admin_home', admin_home, name='admin_home'),
    path('add-staffs', add_staff, name='add-staffs'),
    path('add_staff_save', add_staff_save, name='staff_save'),
    path('add-courses', add_courses, name='add-course'),
    path('add_course_save', add_courses_save, name='course_save'),
    path('add-students', add_students, name='add-students'),
    path('add_students_save', add_students_save, name='student_save'),
]
