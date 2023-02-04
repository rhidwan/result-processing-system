from django.urls import path

from result.views import remove_section_from_score
from .views import *

urlpatterns = [
    # path('basic_info/create/', create_basic_info, name="create_basic_info"),
    path('committee/', exam_committee, name="exam_committee"),
    path('committee/edit/<pk>/', edit_exam_committee, name="edit_exam_committee"),
    path('committee/<pk>/', exam_committe_detail, name="exam_committe_detail"),

    path('course/',  course, name="course"),
    path('course/edit/<pk>/', edit_course, name="edit_course"),
    path('course/<pk>/', course_details, name="course_details"),
    
    path('semester/', semester, name="semester"),
    path('semester/edit/<pk>/', edit_semester, name="edit_semester"),
    path('semester/<pk>/', semester_details, name="semester_details"),

    path('academic_year/', academic_year, name="academic_year"),
    path('academic_year/edit/<pk>/', edit_academic_year, name="edit_academic_year"),
    path('academic_year/<pk>/', academic_year_details, name="academic_year_details"),

    path('score/<student_id>/<course>/', student_course_details, name="student_course_details"),
    path('remove_section/<pk>/<section>/', remove_section_from_score, name="remove_section_from_score"),
]
