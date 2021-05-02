from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect


class LoginCheckMiddleWare(MiddlewareMixin):

    @staticmethod
    def process_view(request, view_func, view_args, view_kwargs):
        module_name = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if module_name == "sdu_beta_web_app.views_admin":
                    pass
                elif module_name == "sdu_beta_web_app.views" or module_name == "django.views.static":
                    pass
                else:
                    return redirect("admin_home")
            elif user.user_type == "2":
                if module_name == "sdu_beta_web_app.views_staff":
                    pass
                elif module_name == "sdu_beta_web_app.views" or module_name == "django.views.static":
                    pass
                else:
                    return redirect("staff_home")
            elif user.user_type == "3":
                if module_name == "sdu_beta_web_app.views_company":
                    pass
                elif module_name == "sdu_beta_web_app.views" or module_name == "django.views.static":
                    pass
                else:
                    return redirect("company_home")
            elif user.user_type == "4":
                if module_name == "sdu_beta_web_app.views_student":
                    pass
                elif module_name == "sdu_beta_web_app.views" or module_name == "django.views.static":
                    pass
                else:
                    return redirect("student_home")
            else:
                return redirect("show_login")

        else:
            if request.path == reverse("show_login") or request.path == reverse("signin") or module_name == "django.contrib.auth.views":
                pass
            else:
                print(request.path)
                return redirect("show_login")
