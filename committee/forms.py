from django import forms
from .models import *

from django import forms

class ExamCommitteeForm(forms.ModelForm):
    class Meta:
        model = ExamCommittee
        exclude = ('id',)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('id',)

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        exclude = ('id',)

class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        exclude = ('id',)
