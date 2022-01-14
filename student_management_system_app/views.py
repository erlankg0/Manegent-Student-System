from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from student_management_system_app.emailBackend import EmailBackends
from student_management_system_app.models import CustomUser


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
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        try:
            if first_name not in ['', None] and last_name not in ['', None] and username not in ['admin', 'Admin', '']:
                if len(password) <= 7 or password in r'[а-яА-ЯёЁ]':
                    messages.error(request,
                                   'The length of password should not be less than 7 characters '
                                   'and should not contain Cyrillic characters')
                    return HttpResponseRedirect('/add-staffs')
                else:
                    user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                      last_name=last_name,
                                                      first_name=first_name, user_type=2)
                    user.staffs.address = address
                    user.save()
                    messages.success(request, 'Successfully Added Staff.')
                    return HttpResponseRedirect('/add-staffs')
        except Exception as Error:
            messages.warning(request, "Error {0}".format(Error))
            return HttpResponseRedirect('/add-staffs')
    else:
        messages.info(request, 'Failed to Add Staff!')
        return HttpResponseRedirect('/add-staffs')
