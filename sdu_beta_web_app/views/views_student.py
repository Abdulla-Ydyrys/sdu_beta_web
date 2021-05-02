
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from sdu_beta_web_app.models import *
from django.core.files.storage import FileSystemStorage
import datetime

def student_home(request):
    return render(request, "student_template/home.html")

def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "student_template/student_profile.html", {"user": user})

def update_student_profile(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        address = request.POST.get("address")
        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = None
        try:
            user = CustomUser.objects.get(id=request.user.id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            student = Students.objects.get(student=request.user.id)

            if picture_url is not None:
                student.display_image = picture_url
            student.address = address
            student.save()
            messages.success(request, "Successfully Edited student profile")
            return HttpResponseRedirect(reverse("student_profile"))
        except:
            messages.error(request, "Failed to Edit student profile")
            return HttpResponseRedirect(reverse("student_profile"))

def student_feedback(request):
    student_id = Students.objects.get(student=request.user.id)
    feedbacks = Students_feedback.objects.filter(student_id=student_id)
    return render(request, "student_template/student_feedback.html", {"feedbacks": feedbacks})

def save_feedback(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_message = request.POST.get("feedback")
        student_id = Students.objects.get(student=request.user.id)
        try:
            feedback = Students_feedback(student_id=student_id, feedback_message=feedback_message, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully  Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed to Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))

def student_registration(request):
    student = Students.objects.get(student=request.user.id)
    expiration_date = Expiration_date.objects.last()
    staffs = CustomUser.objects.filter(user_type=2)
    companies = CustomUser.objects.filter(user_type=3)
    data = Students_registration.objects.filter(student_id=student)
    return render(request, "student_template/student_registration.html", {"data": data, "expiration_date": expiration_date, "staffs": staffs, "companies": companies})

@csrf_exempt
def cancel_registration(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_registration"))
    else:
        try:
            student_id = Students.objects.get(student=request.user.id)
            registration = Students_registration.objects.get(student_id=student_id)
            registration.delete()
            return redirect('/student_registration')
        except:
            return redirect('/student_registration')

def confirm_registration(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_registration"))
    else:
        if request.FILES.get('agreement', False):
            agreement = request.FILES['agreement']
            fs = FileSystemStorage()
            filename = fs.save(agreement.name, agreement)
            agreement_url = fs.url(filename)
        else:
            agreement_url = None
        beta_type = request.POST.get("beta_type")

        supervisor_id = request.POST.get('staffs')
        if not supervisor_id:
            supervisor_id = request.POST.get('companies')
        try:
            supervisor = CustomUser.objects.get(id=supervisor_id)
            student_id = Students.objects.get(student=request.user.id)
            registration = Students_registration(student_id=student_id, agreement=agreement_url, supervisor_id=supervisor, registration_status=0, beta_type=beta_type)
            registration.save()
            messages.success(request, "Successfully Confirmed Registration")
            return HttpResponseRedirect(reverse("student_registration"))
        except:
            messages.error(request, "Failed to Confirm Registration")
            return HttpResponseRedirect(reverse("student_registration"))

def reports(request):
    student = Students.objects.get(student=request.user.id)
    try:
        registered = Students_registration.objects.get(student_id=student)
    except:
        registered = None
    if registered and registered.registration_status == 1:
        report = Reports.objects.all()
        return render(request, "student_template/reports.html", {"report": report, "registered": registered})
    else:
        messages.error(request, "You have not registered, or Your request not yet approved(or rejected)")
        return HttpResponseRedirect(reverse("student_registration"))

def report_detail(request, report_id):
    check_exist = Reports.objects.filter(id=report_id).exists()
    student = Students.objects.get(student=request.user.id)
    try:
        registered = Students_registration.objects.get(student_id=student)
    except:
        registered = None
    if check_exist and registered and registered.registration_status == 1:
        report = Reports.objects.get(id=report_id)
        student = Students.objects.get(student=request.user.id)
        try:
            report_details = Report_submitting.objects.get(report_id=report.id, student_id=student.id)
        except Report_submitting.DoesNotExist:
            report_details = None
        return render(request, "student_template/report_detail.html", {"report": report, "id": report_id, "report_details": report_details})
    elif not registered:
        messages.error(request, "You have not registered, please register first or Your request not yet approved.(or rejected)")
        return HttpResponseRedirect(reverse("student_registration"))
    else:
        return redirect('/reports')

@csrf_exempt
def cancel_report(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("reports"))
    else:
        submit_id = request.POST.get("id")
        try:
            report = Report_submitting.objects.get(id=submit_id)
            report.delete()
            return HttpResponse("True")
        except:
            return HttpResponseRedirect(reverse("reports"))

def submit_report(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("reports"))
    else:
        report_id = request.POST.get("report_id")
        reference = request.POST.get("reference")
        student_id = Students.objects.get(student=request.user.id)
        report = Reports.objects.get(id=report_id)
        try:
            report_submit = Report_submitting(student_id=student_id, report_id=report, submission_status=1, references=reference)
            report_submit.save()
            messages.success(request, "Successfully Submitted Report")
            return HttpResponseRedirect(reverse("report_detail", kwargs={"report_id": report_id}))
        except:
            messages.error(request, "Failed to Submit Report")
            return HttpResponseRedirect(reverse("report_detail", kwargs={"report_id": report_id}))

def grades_list(request):
    student = Students.objects.get(student=request.user.id)
    try:
        registered = Students_registration.objects.get(student_id=student)
    except:
        registered = None
    if registered and registered.registration_status == 1:
        supervisor = CustomUser.objects.get(id=registered.supervisor_id.id)
        reports = Report_submitting.objects.filter(student_id=student)
        grade = 0
        s_mark = 0
        f_mark = 0
        for report in reports:
            grade = grade + report.grade
        grade = grade/15
        grade = round(grade)
        try:
            grade_list = Grades_List.objects.get(student_id=student)
            s_mark = grade_list.supervisor_marks
            f_mark = grade_list.final_marks
        except Grades_List.DoesNotExist:
            grade_list = None
        total = s_mark * 0.6 + grade * 0.15 + f_mark * 0.25
        total = round(total)
        return render(request, "student_template/grades_list.html", {"s_mark": s_mark, "f_mark": f_mark, "grade": grade, "total": total, "supervisor": supervisor, "student": student})
    else:
        messages.error(request, "You have not registered, or Your request not yet approved(or rejected)")
        return HttpResponseRedirect(reverse("student_registration"))