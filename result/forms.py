from django import forms
from .models import *

from django import forms
 
 
# class BasicInfoForms(forms.Form):
class ExamMarkForm(forms.ModelForm):

    class Meta:
        model = ExamMark
        exclude = ('course', 'section' )

class CatmForm(forms.ModelForm):

    class Meta:
        model = Catm
        exclude = ('student', 'total', 'course' )
