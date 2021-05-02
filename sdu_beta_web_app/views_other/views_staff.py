
from django.shortcuts import render, redirect
from django.contrib import messages
from sdu_beta_web_app.models import *
from django.core.files.storage import FileSystemStorage


def staff_home(request):
    return render(request, "staff_template/home.html")


def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "staff_template/staff_profile.html", {"user": user})


def update_staff_profile(request):
    if request.method != "POST":
        return redirect("staff_profile")
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
            staff = Staffs.objects.get(staff=request.user.id)

            if picture_url is not None:
                staff.display_image = picture_url
            staff.address = address
            staff.save()
            messages.success(request, "Successfully Edited Staff Profile")
            return redirect("staff_profile")
        except:
            messages.error(request, "Failed to Edit Staff Profile")
            return redirect("staff_profile")


def my_students(request):
    supervisor = CustomUser.objects.get(id=request.user.id)
    reg = Students_registration.objects.filter(
        supervisor_id=supervisor.id, registration_status=1)
    studentList = Students_registration.objects.filter(
        supervisor_id=supervisor.id, registration_status=1).values_list('student_id', flat=True)
    for s in studentList:
        student = Students.objects.get(id=s)
        try:
            grade_list = Grades_List.objects.get(student_id=s)
        except:
            grade_list = Grades_List(student_id=student)
            grade_list.save()
    grades_list = Grades_List.objects.filter(student_id__in=studentList)
    return render(request, "staff_template/my_students.html", {"reg": reg, "grades_list": grades_list, "studentList": studentList})


def supervisor_grade(request):
    if request.method != "POST":
        return redirect("my_students")
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
                    grades_list = Grades_List(
                        student_id=student, supervisor_marks=g)
                    grades_list.save()
            messages.success(request, "Successfully Set Grade")
            return redirect("my_students")
        except:
            messages.error(request, "Failed to Set Grade")
            return redirect("my_students")
