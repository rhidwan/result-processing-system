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
    
        final_exam_mark = section_a + section_b
        instance.mark_obtained = catm + section_a + section_b
        instance.final_exam_mark = final_exam_mark

    if instance.is_improvement:
        previous_final_exam_mark = instance.previous_score.get("final_exam_mark", 0)
        if previous_final_exam_mark < final_exam_mark:
            instance.is_improved = True
        else:
            instance.is_improved = False
        

    if instance.mark_obtained:
        ccp = instance.course.credit_point
        percentage = (instance.mark_obtained/(ccp *25)) *100
        instance.percentage = percentage
        letter_grade, grade_point = get_letter_grade_point(percentage)
        instance.credit_point = ccp * grade_point
        instance.letter_grade = letter_grade
        instance.grade_point = grade_point
         
    print(sender, instance, "Signal Fired")

@receiver(pre_save, sender=Catm)
def update_catm(sender, instance, **kwargs):
    ccp = instance.course.credit_point
    if ccp == 2:
        ct_marks = sum( instance.ct_1 + instance.ct_2 + instance.ct_3 ) - min(instance.ct_1 + instance.ct_2 + instance.ct_3) 
    elif ccp==3:
        ct_marks = sum( instance.ct_1 + instance.ct_2 + instance.ct_3 + instance.ct_4) - min(instance.ct_1 + instance.ct_2 + instance.ct_3 + instance.ct_4)
    elif ccp==4:
        ct_marks = sum( instance.ct_1 + instance.ct_2 + instance.ct_3 + instance.ct_4) - min(instance.ct_1 + instance.ct_2 + instance.ct_3 + instance.ct_4)
    gross_ct_marks = round(ct_marks/ccp,2)

    instance.total = gross_ct_marks + instance.attendance
    
    print(sender, instance, "Signal Fired")