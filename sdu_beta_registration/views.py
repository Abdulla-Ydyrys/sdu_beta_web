import re

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from django_email_verification import send_email

from sdu_beta_web_app.Email import Email
from sdu_beta_web_app.models import *


def signup_staff(request):
    context = {}
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password1']:
            fullname = request.POST['fullname'].title().split(' ', 1)
            first_name = fullname[0]
            last_name = fullname[1]
            email = request.POST['email'].lower()
            password = request.POST['password']
            if True:  # re.fullmatch(r'^[a-z]+@sdu\.edu\.kz$', email):
                try:
                    user = get_user_model().objects.create_user(
                        username=email, first_name=first_name, last_name=last_name, email=email, password=password, user_type=2)
                    user.is_active = 0
                    send_email(user)
                    messages.success(request, "Email sent")
                    return redirect('show_login')
                except Exception as e:
                    print(e)
                    if e.args[0] == 1062:
                        messages.error(request, "Email allready exists")
                    else:
                        messages.error(request, "Failed to Create Staff")
                    context = {'fullname': f'{first_name} {last_name}',
                               'email': email, 'password': password}
                    return render(request, 'sdu_beta_registration/signup_staff.html', context)
            else:
                messages.error(request, "Email is not SDU Staff's email")
                return render(request, 'sdu_beta_registration/signup_staff.html', context)
        else:
            messages.error(request, 'Check Passwords')
            return render(request, 'sdu_beta_registration/signup_staff.html', context)
    else:
        return render(request, 'sdu_beta_registration/signup_staff.html', context)


def signup_student(request):
    pass


def signup_company(request):
    pass
