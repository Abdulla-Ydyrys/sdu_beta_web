
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from sdu_beta_web_app.models import *
from django.core.files.storage import FileSystemStorage


def company_home(request):
    return render(request, "company_template/home.html")

def company_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "company_template/company_profile.html", {"user": user})

def update_company_profile(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("company_profile"))
    else:
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
            user.save()
            company = Company.objects.get(company=request.user.id)
            if picture_url is not None:
                company.display_image = picture_url
            company.address = address
            company.save()
            messages.success(request, "Successfully Edited company profile")
            return HttpResponseRedirect(reverse("company_profile"))
        except:
            messages.error(request, "Failed to Edit company profile")
            return HttpResponseRedirect(reverse("company_profile"))

def my_interns(request):
    supervisor = CustomUser.objects.get(id=request.user.id)
    reg = Students_registration.objects.filter(supervisor_id=supervisor.id, registration_status=1)
    studentList = Students_registration.objects.filter(supervisor_id=supervisor.id, registration_status=1).values_list('student_id', flat=True)
    for s in studentList:
        student = Students.objects.get(id=s)
        try:
            grade_list = Grades_List.objects.get(student_id=s)
        except:
            grade_list = Grades_List(student_id=student)
            grade_list.save()
    grades_list = Grades_List.objects.filter(student_id__in=studentList)
    return render(request, "company_template/my_interns.html", {"reg": reg, "grades_list": grades_list, "studentList": studentList})

def company_grade(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("my_interns"))
    else:
        try:
            reg_id = request.POST.getlist("reg_id")
            grade = request.POST.getlist("sup_grade")
            zipped_data = zip(reg_id, grade)
            for s, g in zipped_data:
                student = Students.objects.get(id=s)
                try:
                    grades_list = Grades_List.objects.get(student_id=s)
                    grades_list.supervisor_marks = g
                    grades_list.save()
                except Grades_List.DoesNotExist:
                    grades_list = Grades_List(student_id=student, supervisor_marks=g)
                    grades_list.save()
            messages.success(request, "Successfully Set Grade")
            return HttpResponseRedirect(reverse("my_interns"))
        except:
            messages.error(request, "Failed to Set Grade")
            return HttpResponseRedirect(reverse("my_interns"))