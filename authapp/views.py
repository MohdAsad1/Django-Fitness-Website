from django.shortcuts import render, redirect
from django.dispatch import receiver
from django.utils import timezone
import datetime
from datetime import datetime

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from authapp.models import Contact, MembershipPlan, Trainer, Enrollment, Gallery, ExerciseType, Exercise, Attendance


def home(request):
    queryset = ExerciseType.objects.all()
    return render(request, "index.html", {'category': queryset})


def exercise(request, id):
    queryset = Exercise.objects.filter(exercise_type=id)
    return render(request, "exercise.html", {'category': queryset})


def description(request, id):
    queryset = Exercise.objects.filter(id=id)
    return render(request, "description.html", {'category': queryset})


def gallery(request):
    posts = Gallery.objects.all()
    context = {"posts": posts}
    return render(request, "gallery.html", context)


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conform_password = request.POST.get('conform_password')
        if password != conform_password:
            messages.info(request, "Password and Conform Password are Not Same")
            return redirect('/signup')
        try:
            if User.objects.get(username=username):
                messages.warning(request, "User Name Already Exist")
                return redirect('/signup')
        except Exception as e:
            pass
        try:
            if User.objects.get(email=email):
                messages.warning(request, "Email Already Exist")
                return redirect('/signup')
        except Exception as e:
            pass
        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        messages.success(request, "User is Created Please Login")
        return redirect('/login')

    return render(request, "signup.html")


def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        my_user = authenticate(username=username, password=password)
        if my_user is not None:
            login(request, my_user)
            messages.success(request, "Login Successful")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/login')

    return render(request, "handlelogin.html")


def handlelogout(request):
    user_id = request.user.id
    profile = Attendance.objects.filter(user=user_id).last()
    profile.logout_time = timezone.now()
    profile.save()
    logout(request)
    messages.success(request, "Logout Success")
    return redirect('/login')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        number = request.POST.get('num')
        description = request.POST.get('desc')
        myquery = Contact(name=name, email=email, phone_number=number, description=description)
        myquery.save()
        messages.info(request, "Thanks for Contacting us we will get back you soon")
        return redirect('/contact')
    return render(request, "contact.html")


def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login and Try Again")
        return redirect('/login')
    Membership = MembershipPlan.objects.all()
    SelectTrainer = Trainer.objects.all()
    context = {"Membership": Membership, "SelectTrainer": SelectTrainer}
    if request.method == "POST":
        name = request.POST.get('username')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        member = request.POST.get('member')
        trainer = request.POST.get('trainer')
        address = request.POST.get('address')
        query = Enrollment(full_name=name, email=email, gender=gender, date_of_birth=date_of_birth,
                           select_membership_plan=member, select_trainer=trainer, address=address)
        query.save()
        messages.success(request, "Thanks For Enrollment")
        return redirect('/join')
    return render(request, "enroll.html", context)


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login and Try Again")
        return redirect('/login')
    user_name = request.user
    posts = Enrollment.objects.filter(full_name=user_name)
    context = {"posts": posts}
    return render(request, "profile.html", context)


def about(request):
    return render(request, "about.html")


def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login and Try Again")
        return redirect('/login')
    select_trainer = Trainer.objects.all()
    select_exercise = ExerciseType.objects.all()
    context = {"select_trainer": select_trainer, "select_exercise": select_exercise}
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        select_workout = request.POST.get('workout')
        trained_by = request.POST.get('trainer')

        user_instance = User.objects.get(username=user_name)
        workout_instance = ExerciseType.objects.get(name=select_workout)
        trainer_instance = Trainer.objects.get(name=trained_by)

        query = Attendance(user=user_instance, work_out=workout_instance, trainer=trainer_instance)
        query.save()

        profile = Attendance.objects.filter(user=request.user.id).last()
        profile.login_time = timezone.now()
        profile.save()

        messages.warning(request, "Attendance Applied Success")
        return redirect('/attendance')
    return render(request, "attendance.html", context)


def view_attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login and Try Again")
        return redirect('/login')
    if request.method == "POST":
        workout = request.POST.get('workout')
        from_date = request.POST.get('fromdate')
        to_date = request.POST.get('todate')
        search_result = Attendance.objects.filter(login_time__date__range=[from_date, to_date], work_out=workout)
        return render(request, "view_attendance.html", {"attendance": search_result})
    else:
        select_exercise = ExerciseType.objects.all()
        attendance = Attendance.objects.select_related('work_out', 'trainer').all()
        context = {"attendance": attendance, "select_exercise": select_exercise}
        return render(request, "view_attendance.html", context)


