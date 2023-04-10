from django.db import models
import uuid
from committee.models import Course
from students.models import Student
from django.db.models import UniqueConstraint

from user.models import User

# Create your models here.
class Catm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=False)
    attendance = models.FloatField(blank=False, null=False)
    ct_1 = models.FloatField(blank=False, null=False)
    ct_2 = models.FloatField(blank=False, null=False)
    ct_3 = models.FloatField(blank=False, null=False)
    ct_4 = models.FloatField(blank=True, null=True)
    total = models.FloatField(default=0)

class ExamMark(models.Model):
    SECTION_CHOICE = (
        ('A', 'A'),
        ('B', 'B')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, null=False)
    code_no = models.CharField(max_length=50, blank=False, null=False)
    section = models.CharField(max_length=2, choices=SECTION_CHOICE, null=False, blank=False)
    is_allocated = models.BooleanField(default=False)
    marks = models.FloatField()
    is_improvement = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['course',
                'code_no', 'section'],
                name='course_code_no_section_unique',
            ),
        ]


class Score(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code_no = models.CharField(max_length=20, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, null=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False, null=False)
    catm = models.ForeignKey(Catm, on_delete=models.SET_NULL, null=True, blank=True)
    section_a = models.ForeignKey(ExamMark, on_delete=models.SET_NULL, blank=True, null=True, related_name="section_a")
    section_b = models.ForeignKey(ExamMark, on_delete=models.SET_NULL, blank=True, null=True, related_name="section_b")
    final_exam_mark = models.FloatField(blank=True, null=True) #final exam mark $section A + section B
    mark_obtained = models.FloatField(blank=True, null=True) #fem + catm
    percentage = models.FloatField(blank=True, null=True) # mo/25*CR *100
    letter_grade = models.CharField(max_length=4, null=True, blank=True, default='I')
    grade_point = models.FloatField(blank=True, null=True, default=0)
    credit_point = models.FloatField(blank=True, null=True) #credit * grade point
    approved_by = models.ManyToManyField(User, related_name="approved_by")
    
    is_improvement = models.BooleanField(default=False)
    previous_score = models.JSONField(editable=False, blank=True, null=True)
    is_improved = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['course',
                'code_no'],
                name='course_code_no_unique',
            ),
        ]

