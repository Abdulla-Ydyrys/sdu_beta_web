# Django imports
from django.urls import path
# My apps imports
from sdu_beta_web_app.views import views_student

urlpatterns = [
    path('home/', views_student.student_home, name="student_home"),
    path('profile/', views_student.student_profile, name="student_profile"),
    path('update_profile/', views_student.update_student_profile,
         name="update_student_profile"),
    path('student_feedback/', views_student.student_feedback,
         name="student_feedback"),
    path('save_feedback/', views_student.save_feedback, name="save_feedback"),
    path('registration/', views_student.student_registration,
         name="student_registration"),
    path('confirm_registration/', views_student.confirm_registration,
         name="confirm_registration"),
    path('cancel_registration/', views_student.cancel_registration,
         name="cancel_registration"),
    path('reports/', views_student.reports, name="reports"),
    path('report/<str:report_id>/',
         views_student.report_detail, name="report_detail"),
    path('submit_report/', views_student.submit_report, name="submit_report"),
    path('cancel_report/', views_student.cancel_report, name="cancel_report"),
    path('grades_list/', views_student.grades_list, name="grades_list"),
]
