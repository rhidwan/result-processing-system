from result.utils import get_letter_grade_point
from .models import Score, Catm
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Score)
def update_score(sender, instance, **kwargs):
    if instance.course.course_type == "Theory":
        catm = instance.catm.total if instance.catm else 0
        section_a = instance.section_a.marks if instance.section_a else 0
        section_b = instance.section_b.marks if instance.section_b else 0
        
        instance.final_exam_mark = section_a + section_b
        instance.mark_obtained = catm + section_a + section_b
    
    if instance.mark_obtained:
        percentage = (instance.mark_obtained/(instance.course.credit_point*25)) *100
        instance.percentage = percentage
        instance.letter_grade, instance.grade_point = get_letter_grade_point(percentage)
        
    print(sender, instance, "Signal Fired")

@receiver(pre_save, sender=Catm)
def update_catm(sender, instance, **kwargs):
        
    instance.total = instance.ct_1 + instance.ct_2 + instance.ct_3 + instance.attendance
    print(sender, instance, "Signal Fired")