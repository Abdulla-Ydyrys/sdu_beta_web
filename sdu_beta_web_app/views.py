from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from sdu_beta_web_app.Email import Email


def show_login(request):
    return render(request, "login_page.html")


def signin(request):
    if request.method != "POST":
        return redirect('show_login')
    else:
        user = Email.authenticate(request, username=request.POST.get(
            "email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return redirect('admin_home')
            elif user.user_type == "2":
                return redirect("staff_home")
            elif user.user_type == "3":
                return redirect("company_home")
            elif user.user_type == "4":
                return redirect("student_home")
        else:
            messages.error(request, "Не удаётся войти. Пожалуйста, проверьте правильность написания логина и пароля. Возможно, нажата клавиша Caps Lock? Может быть, у Вас включена неправильная раскладка? (русская или английская) Попробуйте набрать свой пароль в текстовом редакторе и скопировать в графу «Пароль» Если Вы всё внимательно проверили, но войти всё равно не удаётся, Вы можете нажать Reset Password.")
            return redirect('show_login')


def log_out(request):
    logout(request)
    return redirect('show_login')


def error_404_view(request, exception):
    context = {'user': request.user}
    return render(request, 'templates_error/error_404.html', context)
