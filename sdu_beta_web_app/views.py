from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib import messages
from sdu_beta_web_app.Email import Email

# Create your views here.


def ShowLogin(request):
    return render(request, "login_page.html")


def Signin(request):
    if request.method != "POST":
        return HttpResponseRedirect('/')
    else:
        user = Email.authenticate(request, username=request.POST.get(
            "email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "3":
                return HttpResponseRedirect(reverse("company_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request, "Не удаётся войти. Пожалуйста, проверьте правильность написания логина и пароля. Возможно, нажата клавиша Caps Lock? Может быть, у Вас включена неправильная раскладка? (русская или английская) Попробуйте набрать свой пароль в текстовом редакторе и скопировать в графу «Пароль» Если Вы всё внимательно проверили, но войти всё равно не удаётся, Вы можете нажать Reset Password.")
            return HttpResponseRedirect("/")


def log_out(request):
    logout(request)
    return HttpResponseRedirect("/")
