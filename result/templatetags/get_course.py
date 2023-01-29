import base64
from django import template
from django.contrib.staticfiles.finders import find as find_static_file

register = template.Library()


@register.simple_tag
def get_course(score, course):
    answers = score.filter(course=course)
    return answers[0] if answers else None

@register.simple_tag
def define(val=None):
  return val