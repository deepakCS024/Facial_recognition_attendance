from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('takeattendance', views.takeattendance, name = 'takeattendance'),
    path('addstudent', views.addstudent, name = 'addstudent'),
    path('searchattendence/', views.searchAttendence, name='searchattendence'),
    path('account/', views.facultyProfile, name='account'),
    path('updateStudentRedirect/', views.updateStudentRedirect, name='updateStudentRedirect'),
    path('updateStudent/', views.updateStudent, name='updateStudent'),
    path('attendence/', views.takeAttendence, name='attendence'),
  
]