# Django imports
from django.urls import path
# My apps imports
from sdu_beta_web_app.views_other import views_company

urlpatterns = [
    path('home/', views_company.company_home, name="company_home"),
    path('profile/', views_company.company_profile, name="company_profile"),
    path('update_profile/', views_company.update_company_profile,
         name="update_company_profile"),
    path('my_interns/', views_company.my_interns, name="my_interns"),
    path('company_grade/', views_company.company_grade, name="company_grade"),
]
