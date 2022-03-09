from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from student_management_system_app.emailBackend import EmailBackends
from student_management_system_app.models import CustomUser, Courses


def show_demo_page(request):
    return render(request, "demo.html")


def show_login_page(request):
    return render(request, "login.html")


def do_login(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Mettod not allow POST</h2>")
    else:
        user = EmailBackends.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user=user)
            return HttpResponseRedirect('/admin_home')
        else:
            messages.error(request, 'Invalid Login Details!')
            return HttpResponseRedirect('/')


def get_user_details(request):
    if request.user != None:
        return HttpResponse(
            "Email : {0} Password : {1}".format(request.POST.get('email'), request.POST.get('password')))
    else:
        return HttpResponse("PLS login first")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def admin_home(request):
    return render(request=request, template_name='hod_templates/html/main_content.html')


def add_staff(request):
    return render(request=request, template_name='hod_templates/html/add_staffs_template.html')


def add_staff_save(request):
    if request.method == "POST":  # проверяем request на наличие метода POST есть True идем ниже если GET False -> else
        first_name = request.POST['first_name']  # получаем данные с формы через request.POST[key]
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        try:
            # Пытаем проверить на валидность данных для сохранения в базу данных
            if first_name not in ['', None] and last_name not in ['', None] and username not in ['admin', 'Admin', '']:
                # если данных не пустые и не зарезирвированые переходит на проверку валидности пароля
                if len(password) <= 7 and password in r'[а-яА-ЯёЁ]':
                    # если длина пароля мешьне или равно 7 и имению кириллицу тогда валидация не проходит!
                    # и возрращяем messages.error и переадрессуем в add-staffs
                    messages.error(request,
                                   'The length of password should not be less than 7 characters '
                                   'and should not contain Cyrillic characters')
                    return HttpResponseRedirect('/add-error')
                else:
                    # в создадим переменную user и сделаем экземпляр класса CustomUser
                    user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                          last_name=last_name,
                                                          first_name=first_name, user_type=2)
                    user.staffs.address = address
                    user.save()
                    # сохраняем
                    messages.success(request, 'Successfully Added Staff.')
                    # Выводим что успешно сохранилось и переадресуем на ссылку добавления персоналла.
                    return HttpResponseRedirect('/add-staffs')
            else:
                # если уже есть такой пользователь тогда не сохраняем а просто переадресуем ссылку и выведим сообщения
                messages.add_message(request, 'Already has is profile {0}'.format(username), 'already')
                return HttpResponseRedirect('/add-staffs')
        except Exception as Error:
            messages.warning(request, "Error {0}".format(Error))
            return HttpResponseRedirect('/add-staffs')
    else:
        messages.info(request, 'Failed to Add Staff!')
        return HttpResponseRedirect('/add-staffs')


def add_courses(request):
    return render(request, template_name='hod_templates/html/add_courses_tempaltes.html')


def add_courses_save(request):
    if request.method == 'POST':
        course_name = request.POST['course']  # получаем данные из формы
        try:
            if course_name != '':  # если форма не пуста сохраняем
                if course_name in Courses.objects.all():
                    messages.add_message(request, 'Already have {0} course'.format(course_name), 'already')
                    return HttpResponseRedirect("/add-courses")
                else:
                    course_model = Courses(course_name=course_name)
                    course_model.save()
                    messages.success(request, 'Successfully Added Course: {0}'.format(course_name))
                    return HttpResponseRedirect('/add-courses')
            else:  # если пуста выводим ошибку но не сохраняем данные
                messages.error(request, 'Can not to be null')
                return HttpResponseRedirect('/add-courses')
        except ValueError:  # ловим ошибки
            messages.warning(request, "Zaten bu kurs var '{0}'".format(course_name))
            return HttpResponseRedirect('/add-courses')
    else:  # если request method не POST выводим ошибку
        messages.error(request, 'Failed Add Courses. Try again')
        return HttpResponseRedirect('/add-courses')


def add_students(request):
    courses = Courses.objects.all()
    context = {'courses': courses}
    return render(request, template_name='hod_templates/html/add_students_templates.html', context=context)


def add_students_save(request):
    if request.method == "POST":  # проверяем request на наличие метода POST есть True идем ниже если GET False -> else
        first_name = request.POST['first_name']  # получаем данные с формы через request.POST[key]
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        gender = request.POST['sex']
        session_start = request.POST['session_start']
        session_end = request.POST['session_end']
        course = request.POST['course']

        # Пытаем проверить на валидность данных для сохранения в базу данных
        try:
            if username not in ['admin', 'Admin', '']:
                # если данных не пустые и не зарезирвированые переходит на проверку валидности пароля
                if len(password) <= 7 and password in r'[а-яА-ЯёЁ]':
                    # если длина пароля мешьне или равно 7 и имению кириллицу тогда валидация не проходит!
                    # и возрращяем messages.error и переадрессуем в add-staffs
                    messages.error(request,
                                   'The length of password should not be less than 7 characters '
                                   'and should not contain Cyrillic characters')
                    return HttpResponseRedirect('/add-students')
                else:
                    # в создадим переменную user и сделаем экземпляр класса CustomUser
                    user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                          last_name=last_name,
                                                          first_name=first_name, user_type=3)
                    user.students.address = address
                    course_obj = Courses.objects.get(id=course)
                    user.students.gender = gender
                    user.students.course_id = course_obj
                    user.students.session_start_year = datetime.strptime(session_start, '%d-%m-%Y').strftime('%Y-%m-%d')
                    user.students.session_end_year = datetime.strptime(session_end, '%d-%m-%Y').strftime('%Y-%m-%d')
                    # user.students.session_start_year = session_start
                    # user.students.session_end_year = session_end
                    user.students.profile_pic = ''
                    user.save()
                    # сохраняем
                    messages.success(request, 'Successfully Added Student.')
                    # Выводим что успешно сохранилось и переадресуем на ссылку добавления персоналла.
                    return HttpResponseRedirect('/add-students')
            else:
                # если уже есть такой пользователь тогда не сохраняем а просто переадресуем ссылку и выведим сообщения
                messages.add_message(request, 'Can not to be as {}'.format(username), 'already')
                return HttpResponseRedirect('/add-students')
        except Exception as Error:
            messages.warning(request, "{}".format(Error))
            return HttpResponseRedirect('/add-students')

    else:
        messages.info(request, 'Failed to Add Student!')
        return HttpResponseRedirect('/add-students')
