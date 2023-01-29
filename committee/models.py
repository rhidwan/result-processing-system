from django.db import models

from user.models import User
import uuid

class AcademicYear(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    class Meta:
        get_latest_by = "-name"

    def __str__(self):
        return self.name


class Semester(models.Model):
    SEMESTER_CHOICE = (
        ('1st', '1st'),
        ('2nd', '2nd'),
        ('3rd', '3rd'),
        ('4th', '4th'),
        ('5th', '5th'),
        ('6th', '6th'),
        ('7th', '7th'),
        ('8th', '8th'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, choices=SEMESTER_CHOICE, null=False, blank=False)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, blank=True, null=True )

    class Meta:
        ordering = ("-academic_year", 'name')


class ExamCommittee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, blank=True, null=True )
    semester = models.ManyToManyField(Semester, related_name="semester")
    member = models.ManyToManyField(User, related_name="exam_committee_member")
    chairman = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

class Course(models.Model):  
    TYPE_CHOICE = (
        ('Theory', 'Theory'),
        ('Lab/FieldWork/Project', 'Lab/FieldWork/Project')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    examiner = models.ManyToManyField(User, related_name="examiner")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=False, blank=False)
    credit_point = models.IntegerField()
    course_type = models.CharField(max_length=40, choices=TYPE_CHOICE, null=False, default='Theory', blank=False)
    def __str__(self):
        return self.course_code

