from django.urls import path
from authapp import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('login', views.handlelogin, name="handlelogin"),
    path('logout/', views.handlelogout, name="handlelogout"),
    path('contact', views.contact, name="contact"),
    path('join', views.enroll, name="enroll"),
    path('profile', views.profile, name="profile"),
    path('gallery', views.gallery, name="gallery"),
    path('about', views.about, name="about"),
    path('attendance', views.attendance, name="attendance"),
    path('viewattendance', views.view_attendance, name="view_attendance"),
    path('exercise/<int:id>/', views.exercise, name='exercise'),
    path('description/<int:id>/', views.description, name='description'),

]
