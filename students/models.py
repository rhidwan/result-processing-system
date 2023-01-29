from django.db import models
from django_resized import ResizedImageField
from user.models import User
import uuid
# Create your models here.
class Hall(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False)

class Student(models.Model):
    TYPE_CHOICE = (
        ('BSc', 'BSc'),
        ('MSc', 'MSc')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=250, null=False, blank=False)
    student_id =  models.CharField(max_length=10, null=False, blank=False, unique=True)
    degree = models.CharField(max_length=20, choices=TYPE_CHOICE, null=False, blank=False)
    session = models.CharField(max_length=50, null=False, blank=False)
    hall= models.ForeignKey(Hall, on_delete=models.SET_NULL, blank=True, null=True )
    
    



