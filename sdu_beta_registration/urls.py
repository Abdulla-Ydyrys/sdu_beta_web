from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('staff/', views.signup_staff, name='signup_staff'),
    path('student/', views.signup_student, name='signup_student'),
    path('company/', views.signup_company, name='signup_company'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
