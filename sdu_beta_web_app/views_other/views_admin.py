# Django imports
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# My app imports
from sdu_beta_web_app.models import *
from sdu_beta_web_app.filters import RegistrationFilter, StudentFilter, ReportFilter
from sdu_beta_web_app.tables import tables_admin as tables


def admin_home(request):
    return render(request, "admin_template/home.html")


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "admin_template/admin_profile.html", {"user": user})


def update_admin_profile(request):
    if request.method != "POST":
        return redirect("admin_profile")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
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
            admin = Admin.objects.get(admin=request.user.id)

            if picture_url is not None:
                admin.display_image = picture_url
            admin.save()
            messages.success(request, "Successfully Edited Admin")
            return redirect("admin_profile")
        except Exception:
            messages.error(request, "Failed to Edit Admin")
            return redirect("admin_profile")


def add_staff(request):
    return render(request, "admin_template/add_staff.html")


def save_staff(request):
    if request.method != "POST":
        return redirect("add_staff")
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = None
        try:
            user = CustomUser.objects.create_user(email=email, password=password, username=username,
                                                  last_name=last_name, first_name=first_name, user_type=2)
            user.staffs.address = address
            user.staffs.gender = gender
            user.staffs.display_image = picture_url
            user.save()
            messages.success(request, "Successfully Added Staff")
            return redirect("manage_staff")
        except:
            messages.error(request, "Failed to Add Staff")
            return redirect("add_staff")


def manage_staff(request):
    table = tables.StaffsTable(Staffs.objects.all())
    context = {'table': table}
    return render(request, "admin_template/manage_staff.html", context)


def edit_staff(request, staff_id):
    try:
        staff = Staffs.objects.get(staff=staff_id)
        return render(request, "admin_template/edit_staff.html", {"staff": staff, "id": staff_id})
    except:
        return redirect('manage_staff')


def update_staff(request):
    if request.method != "POST":
        return redirect("edit_staff")
    else:
        staff_id = request.POST.get("staff_id")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = None
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()

            staff = Staffs.objects.get(staff=staff_id)
            staff.address = address
            staff.gender = gender
            if picture_url is not None:
                staff.display_image = picture_url
            staff.save()
            messages.success(request, "Successfully Edited Staff")
            return redirect("manage_staff")
        except:
            messages.error(request, "Failed to Edit Staff")
            return redirect("edit_staff", staff_id=staff_id)


def delete_staff(request, staff_id):
    try:
        staff = Staffs.objects.get(staff=staff_id)
        staff.delete()
        user = CustomUser.objects.get(id=staff_id)
        user.delete()
        return redirect('manage_staff')
    except:
        return redirect('manage_staff')


def add_company(request):
    return render(request, "admin_template/add_company.html")


def save_company(request):
    if request.method != "POST":
        return redirect("add_company")
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
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
            user = CustomUser.objects.create_user(
                email=email, password=password, username=username, user_type=3)
            user.company.address = address
            user.company.display_image = picture_url
            user.save()
            messages.success(request, "Successfully Added Company")
            return redirect("manage_company")
        except:
            messages.error(request, "Failed to Add Company")
            return redirect("add_company")


def manage_company(request):
    companies = Company.objects.all()
    return render(request, "admin_template/manage_company.html", {"companies": companies})


def edit_company(request, company_id):
    try:
        company = Company.objects.get(company=company_id)
        return render(request, "admin_template/edit_company.html", {"company": company, "id": company_id})
    except:
        return redirect('manage_company')


def update_company(request):
    if request.method != "POST":
        return redirect("edit_company")
    else:
        company_id = request.POST.get("company_id")
        email = request.POST.get("email")
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
            user = CustomUser.objects.get(id=company_id)
            user.email = email
            user.username = username
            user.save()

            company = Company.objects.get(company=company_id)
            company.address = address
            if picture_url is not None:
                company.display_image = picture_url
            company.save()
            messages.success(request, "Successfully Edited Company")
            return redirect("manage_company")
        except:
            messages.error(request, "Failed to Edit Company")
            return redirect("edit_company", company_id=company_id)


def delete_company(request, company_id):
    try:
        company = Company.objects.get(company=company_id)
        company.delete()
        user = CustomUser.objects.get(id=company_id)
        user.delete()
        return redirect('manage_company')
    except:
        return redirect('manage_company')


def add_student(request):
    return render(request, "admin_template/add_student.html")


def save_student(request):
    if request.method != "POST":
        return redirect("add_student")
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        address = request.POST.get("address")
        gender = request.POST.get("gender")

        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = None
        try:
            user = CustomUser.objects.create_user(email=email, password=password, username=username,
                                                  last_name=last_name, first_name=first_name, user_type=4)
            user.students.address = address
            user.students.gender = gender
            user.students.display_image = picture_url
            user.save()
            messages.success(request, "Successfully Added Student")
            return redirect("manage_student")
        except:
            messages.error(request, "Failed to Add Student")
            return redirect("add_student")


def manage_student(request):
    students = Students.objects.all()
    return render(request, "admin_template/manage_student.html", {"students": students})


def edit_student(request, student_id):
    try:
        student = Students.objects.get(student=student_id)
        return render(request, "admin_template/edit_student.html", {"student": student, "id": student_id})
    except:
        return redirect('manage_student')


def update_student(request):
    if request.method != "POST":
        return redirect("edit_student")
    else:
        student_id = request.POST.get("student_id")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        if request.FILES.get('picture', False):
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            filename = fs.save(picture.name, picture)
            picture_url = fs.url(filename)
        else:
            picture_url = None
        try:
            user = CustomUser.objects.get(id=student_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()

            student = Students.objects.get(student=student_id)
            student.address = address
            student.gender = gender
            if picture_url is not None:
                student.display_image = picture_url
            student.save()
            messages.success(request, "Successfully Edited Student")
            return redirect("manage_student")
        except:
            messages.error(request, "Failed to Edit Student")
            return redirect("edit_student", student_id=student_id)


def delete_student(request, student_id):
    try:
        student = Students.objects.get(student_id=student_id)
        student.delete()
        user = CustomUser.objects.get(id=student_id)
        user.delete()
        return redirect('manage_student')
    except:
        return redirect('manage_student')


def feedback_messages(request):
    feedbacks = Students_feedback.objects.all()
    return render(request, "admin_template/feedback_messages.html", {"feedbacks": feedbacks})


@csrf_exempt
def feedback_reply(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:
        feedback = Students_feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return redirect("feedback_messages")


def set_end_date(request):
    if request.method != "POST":
        return redirect("manage_registration")
    else:
        end_date = request.POST.get("expiry_date")
        try:
            exp_date = Expiration_date(end_date=end_date)
            exp_date.save()
            messages.success(request, "Successfully set registration date")
            return redirect("manage_registration")
        except:
            messages.error(request, "Failed To set registration date")
            return redirect("manage_registration")


def manage_registration(request):
    registrations = Students_registration.objects.all()
    my_filter = RegistrationFilter(request.GET, queryset=registrations)
    registrations = my_filter.qs
    exp_date = Expiration_date.objects.last()
    return render(request, "admin_template/manage_registration.html",
                  {"registrations": registrations, "exp_date": exp_date, "my_filter": my_filter})


def reg_approve(request, student_id):
    try:
        registration = Students_registration.objects.get(student_id=student_id)
        registration.registration_status = 1
        registration.save()
        return redirect('manage_registration')
    except:
        return redirect('manage_registration')


def reg_reject(request, student_id):
    try:
        registration = Students_registration.objects.get(student_id=student_id)
        registration.registration_status = 2
        registration.save()
        return redirect('manage_registration')
    except:
        return redirect('manage_registration')


def reg_cancel(request, student_id):
    try:
        registration = Students_registration.objects.get(student_id=student_id)
        registration.registration_status = 0
        registration.reject_reason = ""
        registration.save()
        return redirect('manage_registration')
    except:
        return redirect('manage_registration')


@csrf_exempt
def reject_reply(request):
    registration_id = request.POST.get("id")
    reject_reason = request.POST.get("message")
    try:
        registration = Students_registration.objects.get(id=registration_id)
        registration.reject_reason = reject_reason
        registration.save()
        return HttpResponse("True")
    except:
        return redirect("manage_registration")


def add_report(request):
    return render(request, "admin_template/add_report.html")


def save_report(request):
    if request.method != "POST":
        return redirect("add_report")
    else:
        report_name = request.POST.get("report_name")
        report_detail = request.POST.get("report_detail")
        due_date = request.POST.get("due_date")
        try:
            report = Reports(report_name=report_name,
                             report_detail=report_detail, due_date=due_date)
            report.save()
            messages.success(request, "Successfully Added Report")
            return redirect("manage_report")
        except:
            messages.error(request, "Failed to Add Report")
            return redirect("add_report")


def manage_report(request):
    reports = Reports.objects.all()
    return render(request, "admin_template/manage_report.html", {"reports": reports})


def edit_report(request, report_id):
    try:
        report = Reports.objects.get(id=report_id)
        return render(request, "admin_template/edit_report.html", {"report": report, "id": report_id})
    except:
        return redirect('manage_report')


def update_report(request):
    if request.method != "POST":
        return redirect("manage_report")
    else:
        report_id = request.POST.get("report_id")
        report_name = request.POST.get("report_name")
        report_detail = request.POST.get("report_detail")
        due_date = request.POST.get("due_date")
        try:
            report = Reports.objects.get(id=report_id)
            report.report_name = report_name
            report.report_detail = report_detail
            report.due_date = due_date
            report.save()
            messages.success(request, "Successfully Updated Report")
            return redirect("manage_report")
        except:
            messages.error(request, "Failed to Updated Report")
            return redirect("manage_report")


def delete_report(request, report_id):
    try:
        report = Reports.objects.get(id=report_id)
        report.delete()
        messages.success(request, "Report is deleted")
        return redirect("manage_report")
    except:
        messages.error(request, "Report doesn't exist")
        return redirect("manage_report")


def view_report(request, report_id):
    reports = Report_submitting.objects.filter(report_id=report_id)
    my_filter = ReportFilter(request.GET, queryset=reports)
    reports = my_filter.qs
    report_id = Reports.objects.get(id=report_id)
    return render(request, "admin_template/view_report.html",
                  {"reports": reports, "report_id": report_id, "my_filter": my_filter})


def set_grade(request):
    if request.method != "POST":
        return redirect("manage_report")
    else:
        report_id = request.POST.get("report_id")
        try:
            submit_id = request.POST.getlist("submit_id")
            grade = request.POST.getlist("grade")
            zipped_data = zip(submit_id, grade)

            for s, g in zipped_data:
                submit_report = Report_submitting.objects.get(id=s)
                if submit_report.submission_status == 0:
                    continue
                else:
                    submit_report.grade = g
                    submit_report.submission_status = 2
                    submit_report.save()
            messages.success(request, "Successfully Set Grade")
            return redirect("view_report", report_id=report_id)
        except:
            messages.error(request, "Failed to Set Grade")
            return redirect("view_report", report_id=report_id)


def grades(request):
    registrations = Students_registration.objects.filter(registration_status=1)
    my_filter = RegistrationFilter(request.GET, queryset=registrations)
    registrations = my_filter.qs
    return render(request, "admin_template/grades.html", {"registrations": registrations, "my_filter": my_filter})


def view_grade(request, student_id):
    try:
        student = Students.objects.get(student=student_id)
        registered = Students_registration.objects.get(student_id=student)
    except:
        student = None
        registered = None
    if registered and registered.registration_status == 1:
        supervisor = CustomUser.objects.get(id=registered.supervisor_id.id)
        reports = Report_submitting.objects.filter(student_id=student)
        grade = 0
        s_mark = 0
        f_mark = 0
        for report in reports:
            grade = grade + report.grade
        grade = grade / 15
        grade = round(grade)
        try:
            grade_list = Grades_List.objects.get(student_id=student)
            s_mark = grade_list.supervisor_marks
            f_mark = grade_list.final_marks
        except Grades_List.DoesNotExist:
            grade_list = Grades_List(student_id=student)
            grade_list.save()
        total = s_mark * 0.6 + grade * 0.15 + f_mark * 0.25
        total = round(total)
        return render(request, "admin_template/grades_list.html",
                      {"s_mark": s_mark, "f_mark": f_mark, "grade": grade, "total": total, "supervisor": supervisor,
                       "id": student_id, "student": student, "grade_list": grade_list})
    else:
        return redirect("grades")


@csrf_exempt
def set_final_grade(request):
    if request.method != "POST":
        return redirect("grades")
    else:
        grade_id = request.POST.get("grade_id")
        student_id = request.POST.get("student_id")
        final_grade = request.POST.get("final_grade")
        try:
            grade = Grades_List.objects.get(id=grade_id)
            grade.final_marks = final_grade
            grade.save()
            return HttpResponse("True")
        except:
            return redirect("view_grade", student_id=student_id)


@csrf_exempt
def reset_final_grade(request):
    if request.method != "POST":
        return redirect("grades")
    else:
        grade_id = request.POST.get("grade_id")
        student_id = request.POST.get("student_id")
        try:
            grade = Grades_List.objects.get(id=grade_id)
            grade.final_marks = 0
            grade.save()
            return HttpResponse("True")
        except:
            return redirect("view_grade", student_id=student_id)
