# Django imports
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Installed Apps imports
from django_email_verification import urls as email_urls

urlpatterns = [
    # Base paths
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('/', include('sdu_beta_web_app.urls')),
    # Registration paths
    path('signup/', include('sdu_beta_registration.urls')),
    # Admin paths
    path('admin/', include('sdu_beta_web_app.urls_other.urls_admin')),
    # Staff paths
    path('staff/', include('sdu_beta_web_app.urls_other.urls_staff')),
    # Company paths
    path('company/', include('sdu_beta_web_app.urls_other.urls_company')),
    # Student paths
    path('student/', include('sdu_beta_web_app.urls_other.urls_student')),
    # Intalled apps' paths
    path('email/', include(email_urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
