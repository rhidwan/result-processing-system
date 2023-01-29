import base64
from django import template
from django.contrib.staticfiles.finders import find as find_static_file

register = template.Library()

@register.simple_tag
def calculate_catm(catm):
    total = 0
    total += catm.attendance + catm.ct_1 + catm.ct_2 + catm.ct_3
    return total

@register.simple_tag
def calculate_gpa(scores, semester):
    '''
    gps = Sum(CG)/Sum(C)
    '''
    sum_cg = sum([score.course.credit_point * score.grade_point for score in scores if score.grade_point])
    sum_c = sum([course.credit_point for course in semester.course_set.all()])

    gpa =round( sum_cg / sum_c, 2)
    status = "F" if gpa < 2.20 else 'P'
    return gpa, status

@register.simple_tag
def calculate_credit_offered(semester):
    courses = semester.course_set.all()
    return sum([x.credit_point for x in courses])

@register.simple_tag
def calculate_credit_earned(scores):
    return sum([score.course.credit_point  for score in scores if score.grade_point and score.grade_point > 0 ])

@register.simple_tag
def define(val=None):
    return val

@register.filter
def hash(h, key):
    data = h.get(key, "")
    # if type(data) == list:
    #     return data[0]
    return data