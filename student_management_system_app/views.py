from django.contrib.auth import login, logout
from django.contrib import messages
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
        course_name = request.POST['course']
        try:
            course = Courses.objects.create(course_name=course_name)
            course.save()
            messages.success(request, 'Successfully Added Course: {0}'.format(course))
            return HttpResponseRedirect('/add-courses')
        except Exception as Error:
            messages.warning(request, Error)
            return HttpResponseRedirect('/add-courses')
    else:
        messages.error(request, 'Failed Add Courses. Try again')
        return HttpResponseRedirect('/add-courses')
