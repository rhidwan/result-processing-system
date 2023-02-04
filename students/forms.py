from django import forms
from .models import *


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('id',)

class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        exclude = ('id',)


