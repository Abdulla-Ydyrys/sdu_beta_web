from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUser(AbstractUser):
    user_types = ((1, "Admin"), (2, "Staff"), (3, "Company"), (4, "Student"))
    user_type = models.CharField(default=1, choices=user_types, max_length=10)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    display_image = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Staffs(models.Model):
    staff = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255)
    display_image = models.FileField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Company(models.Model):
    company = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    display_image = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Vacancy(models.Model):
    vacancy_name = models.CharField(max_length=255)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.TextField()
    requirements = models.TextField()
    amount = models.TextField()
    action = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Students(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255)
    display_image = models.FileField()
    address = models.TextField()
    vacancy_id = models.ForeignKey(
        Vacancy, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s' % (self.student.first_name, self.student.last_name)


class Grades_List(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    final_marks = models.IntegerField(default=0)
    supervisor_marks = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)


class Students_registration(models.Model):
    STATUS = (
        ('SDU Beta', 'SDU Beta'),
        ('Academic Beta', 'Academic Beta'),
        ('Industrial Beta', 'Industrial Beta'),
    )

    REG_STATUS = (
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Rejected'),
    )

    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    supervisor_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    beta_type = models.CharField(max_length=255, choices=STATUS)
    agreement = models.FileField()
    registration_status = models.IntegerField(default=0, choices=REG_STATUS)
    reject_reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Expiration_date(models.Model):
    end_date = models.DateTimeField()


class Students_feedback(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback_message = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Students_notification(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Staff_notification(models.Model):
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Company_notification(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Reports(models.Model):
    report_name = models.CharField(max_length=255)
    report_detail = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Report_submitting(models.Model):
    SUB_STATUS = (
        (0, 'Not Submitted'),
        (1, 'Submitted'),
        (2, 'Graded'),
    )
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    report_id = models.ForeignKey(Reports, on_delete=models.CASCADE)
    references = models.CharField(max_length=255)
    submission_status = models.IntegerField(default=0, choices=SUB_STATUS)
    grade = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Policy(models.Model):
    policy_name = models.CharField(max_length=255)
    policy = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(staff=instance)
        if instance.user_type == 3:
            Company.objects.create(company=instance)
        if instance.user_type == 4:
            Students.objects.create(student=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.company.save()
    if instance.user_type == 4:
        instance.students.save()
