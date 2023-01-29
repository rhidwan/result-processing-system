from django.urls import path
from .views import *

urlpatterns = [

    path('student/', student, name="student"),
    path('student/edit/<pk>/', edit_student, name="edit_student"),
    path('student/<student_id>/', student_detail, name="student_detail"),
    path('hall/',  hall, name="hall"),
    path('hall/<pk>/', hall_detail, name="hall_detail"),
    
]