from django.urls import path
from .views import *

urlpatterns = [
    # path('basic_info/create/', create_basic_info, name="create_basic_info"),
    path('catm/', catm, name="catm"),
    path('catm/<pk>/', catm_detail, name="catm_detail"),
    path('catm/<pk>/edit/', edit_catm, name="edit_catm"),

    path('exam_mark/', exam_mark, name="exam_mark"),
    path('exam_mark/<pk>/', catm_detail, name="exam_mark_detail"),
    path('exam_mark/<pk>/edit/', edit_exam_mark, name="edit_exam_mark"),
    
    path('non_theory_mark', non_theory_mark, name="non_theory_mark"),
    path('id_code_mappng/', id_code_mapping, name="id_code_mapping"),

    path('result/', result, name="result"),

    path('score/',  score, name="score"),
    path('score/<pk>/', score_detail, name="score_detail"),
    
    path('grade_sheet/<semester>/<student_id>/', generate_grade_sheet, name="generate_grade_sheet"),
    path('tabulation_sheet/<semester>/', generate_tabulation_sheet, name="generate_tabulation_sheet"),

    path('excel/import/', import_from_excel, name="import_score_from_excel"),
]