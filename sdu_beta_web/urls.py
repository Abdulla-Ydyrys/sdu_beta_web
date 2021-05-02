# Django imports
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# My apps imports
from sdu_beta_web_app import views, views_staff, views_company, views_student
# Installed Apps imports
from django_email_verification import urls as email_urls

urlpatterns = [
    # Base paths
    path('', views.ShowLogin, name="show_login"),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('sign_in', views.Signin, name="sign_in"),
    path('log_out', views.log_out, name="logout"),
    # Registration paths
    path('signup/', include('sdu_beta_registration.urls')),
    # Admin paths
    path('admin/', include('sdu_beta_web_app.urls.urls_admin')),
    # Staff paths
    path('staff/', include('sdu_beta_web_app.urls.urls_staff')),
    # Company paths
    path('company/', include('sdu_beta_web_app.urls.urls_company')),
    # Student paths
    path('student/', include('sdu_beta_web_app.urls.urls_student')),
    # Intalled apps' paths
    path('email/', include(email_urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
