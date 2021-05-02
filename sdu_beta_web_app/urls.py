# Django imports
from django.urls import path
# My apps imports
from sdu_beta_web_app import views

urlpatterns = [
    path('', views.show_login, name="show_login"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.logout, name="logout"),
]
