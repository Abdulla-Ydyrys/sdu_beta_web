# Django imports
from django.urls import path
# My apps imports
from sdu_beta_web_app.views import views_staff

urlpatterns = [
    path('home/', views_staff.staff_home, name="staff_home"),
    path('profile/', views_staff.staff_profile, name="staff_profile"),
    path('update_profile/', views_staff.update_staff_profile,
         name="update_staff_profile"),
    path('my_students/', views_staff.my_students, name="my_students"),
    path('supervisor_grade/', views_staff.supervisor_grade, name="supervisor_grade"),
]
