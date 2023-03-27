import base64
from django import template
from django.contrib.staticfiles.finders import find as find_static_file

register = template.Library()

@register.simple_tag
def calculate_catm(catm):
    total = 0
    try:
        total += catm.attendance + catm.ct_1 + catm.ct_2 + catm.ct_3
    except:
        total = ""
    return total

@register.simple_tag
def calculate_credit_point(gpa, cp):
    try:
        gpa = float(gpa)
    except:
        gpa = 0
    return gpa * cp

@register.simple_tag
def get_grade_point(score):
    if score.is_improvement:
        if not score.is_improved:
            return score.previous_score['grade_point']
        
    return score.grade_point

@register.simple_tag
def get_score_improvement(score):
    print(score)
    try:
        if score.is_improvement:
            if not score.is_improved:
                return score.previous_score
    except:
        pass
    return score

@register.simple_tag
def calculate_gpa(scores, semester):
    '''
    gps = Sum(CG)/Sum(C)
    '''

    if type(scores) == dict:
        new_scores = []
        for k,v in scores.items():
            new_scores += v
        scores = new_scores
    

    sum_cg = sum([score.course.credit_point * get_grade_point(score) for score in scores if get_grade_point(score)])
    sum_c = sum([course.credit_point for course in semester.course_set.all()])

    gpa =round( sum_cg / sum_c, 2)
    status = "F" if gpa < 2.20 else 'P'
    return gpa, status


@register.simple_tag
def get_unallocated_course(semester, scores=[]):
    score_courses = [x.course for x in scores]
    return  [ x for x in  semester.course_set.all() if x not in score_courses]

@register.simple_tag
def calculate_credit_offered(semester=None, courses=None):
    if semester:
        courses = semester.course_set.all()

    return sum([x.credit_point for x in courses])

@register.simple_tag
def calculate_credit_earned(scores):
    if type(scores) == dict:
        new_scores = []
        for k,v in scores.items():
            new_scores += v
        scores = new_scores
        
    return sum([score.course.credit_point  for score in scores if get_grade_point(score) and get_grade_point(score) > 0 ])

@register.simple_tag
def define(val=None):
    return val

@register.simple_tag
def multiply(a, b):
    return a*b
    
@register.filter
def hash(h, key):
    data = h.get(key, "")
    # if type(data) == list:
    #     return data[0]
    return data

@register.simple_tag
def chunks(lst, chunk_size):
    if type(lst) != list:
        lst = list(lst)

    return [lst[i:i+4] for i in range(0, len(lst), chunk_size)]