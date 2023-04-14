from distutils.command.upload import upload
from django.db import models
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User


class ExerciseType(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to='gallery')
    exercise_type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=1000)
    video = models.FileField(upload_to='gallery/%y')

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    description = models.TextField()

    def __str__(self):
        return self.name + "-" + self.email


class Enrollment(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    TYPE_CHOICE = (
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("NOT TO SAY", "NOT TO SAY")
    )
    gender = models.CharField(max_length=30, choices=TYPE_CHOICE, default='MALE')
    date_of_birth = models.CharField(max_length=50)
    select_membership_plan = models.CharField(max_length=200)
    select_trainer = models.CharField(max_length=55)
    address = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.full_name


class Trainer(models.Model):
    name = models.CharField(max_length=55)
    TYPE_CHOICE = (
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("NOT TO SAY", "NOT TO SAY")
    )
    gender = models.CharField(max_length=30, choices=TYPE_CHOICE, default='MALE')
    phone = models.CharField(max_length=25)
    salary = models.IntegerField()
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class MembershipPlan(models.Model):
    plan = models.CharField(max_length=185)
    price = models.IntegerField()

    def __int__(self):
        return self.id


class Gallery(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to='gallery')
    time_stamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __int__(self):
        return self.title


class Attendance(models.Model):
    login_time = models.DateTimeField(null=True, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    logout_time = models.DateTimeField(null=True, default=None, blank=True)
    work_out = models.ForeignKey(ExerciseType, on_delete=models.CASCADE, null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True)

    def __int__(self):
        return self.user
