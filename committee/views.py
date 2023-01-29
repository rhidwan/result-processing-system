from itertools import groupby
from operator import itemgetter
from django.shortcuts import render
from committee.forms import AcademicYearForm, CourseForm, ExamCommitteeForm, SemesterForm
from django.http import Http404, HttpResponse, JsonResponse
from result.models import Catm, ExamMark, Score

from user.models import User
from .models import AcademicYear, Course, ExamCommittee, Semester
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse


# Create your views here.
def exam_committee(request):
    if request.method == "GET":
    #list
        committies = ExamCommittee.objects.all()
        teachers = User.objects.all()
        semesters = Semester.objects.all()
        academic_years = AcademicYear.objects.all()
        print(academic_years)
        return render(request, "committee.html", {"committies": committies, "teachers": teachers, "semesters": semesters, 'academic_years': academic_years})
    
    elif request.method == "POST":
        print(request.POST)
        academic_year, created = AcademicYear.objects.get_or_create(request.POST.get('academic_year', None))
        
        # updated_request = request.POST.copy()
        # updated_request.update({'academic_year': academic_year.id})
        # committee = ExamCommitteeForm(updated_request)
        committee = ExamCommitteeForm(request.POST)
        

        if committee.is_valid():
            committee.save()
            messages.success(request, "Successfully Updated Commttee")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)
       
        else:
            messages.error(request, "Failed To Update Commttee Information")
            err_msg = ""
            for field, errors in committee.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)


@login_required()
def edit_exam_committee(request, pk):
    exam_committee = get_object_or_404(ExamCommittee, id=pk)
    if request.method == "GET":
        committies = ExamCommittee.objects.all()
        teachers = User.objects.all()
        semesters = Semester.objects.all()
        academic_years = AcademicYear.objects.all()

        return render(request, 'form/committee_form.html', {
            "action": reverse('edit_exam_committee', args=[pk]),
            "committee": exam_committee,
            "teachers": teachers, 
            "semesters": semesters,
            'academic_years': academic_years
        })

    if request.method == "POST":
        form = ExamCommitteeForm(request.POST, instance=exam_committee)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update Work Experience")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    
    if request.method == "DELETE":
        try:
            exam_committee.delete()
            
            messages.success(request, "Successfully Deleted")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Update Work Experience")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)


def exam_committe_detail(request, pk):

    return render(request, "committee_detail.html")

    
def course(request):
    if request.method == "GET":
    #list
        courses = Course.objects.all()
        teachers = User.objects.all()
        semesters = Semester.objects.all()
        academic_years = AcademicYear.objects.all()


        return render(request, "course.html", {"courses": courses, "teachers": teachers, "semesters": semesters, 'academic_years': academic_years})
    
    elif request.method == "POST":
        print(request.POST)
        course = CourseForm(request.POST)
        if course.is_valid():
            course.save()
            messages.success(request, "Successfully Updated Transaction Detail")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)
       
        else:
            messages.error(request, "Failed To Update Educational Background")
            err_msg = ""
            for field, errors in course.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)


def course_details(request, pk):
    course = get_object_or_404(Course, id=pk)
    scores = Score.objects.filter(course=course).prefetch_related('catm', 'catm__student')
    exam_marks = ExamMark.objects.filter(course=course)
    return render(request, 'course_details.html', {"course": course, "scores": scores, "exam_marks": exam_marks})


@login_required()
def edit_course(request, pk):
    course = get_object_or_404(Course, id=pk)
    if request.method == "GET":
        # committies = ExamCommittee.objects.all()
        teachers = User.objects.all()
        semesters = Semester.objects.all()
        academic_years = AcademicYear.objects.all()

        return render(request, 'form/course_form.html', {
            "action": reverse('edit_course', args=[pk]),
            "course": course,
            "teachers": teachers, 
            "semesters": semesters,
            'academic_years': academic_years
        })

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update Work Experience")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    
    if request.method == "DELETE":
        try:
            course.delete()
            
            messages.success(request, "Successfully Deleted")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Update Work Experience")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)

def semester(request):
    if request.method == "GET":
        semesters = Semester.objects.all()
        academic_years = AcademicYear.objects.all()

        return render(request, 'semesters.html', {
            "semesters": semesters,
            "semester_options": ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th'],
            'academic_years': academic_years,
            
            })

    elif request.method == "POST":
        semester = SemesterForm(request.POST)
        if semester.is_valid():
            semester.save()
            messages.success(request, "Successfully Updated Semester Info")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)
       
        else:
            messages.error(request, "Failed To Update Semester Info")
            err_msg = ""
            for field, errors in semester.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)

@login_required()   
def edit_semester(request, pk):
    semester = get_object_or_404(Semester, id=pk)
    if request.method == "GET":
        # committies = ExamCommittee.objects.all()
        academic_years = AcademicYear.objects.all()

        return render(request, 'form/semester_form.html', {
            "action": reverse('edit_semester', args=[pk]),
            "semester": semester,
            "semester_options": ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th'],
            'academic_years': academic_years
        })

    if request.method == "POST":
        form = SemesterForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update Semester Details")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    
    if request.method == "DELETE":
        try:
            semester.delete()
            
            messages.success(request, "Successfully Deleted")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Update Semester Details")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)

@login_required()
def semester_details(request, pk):
    try:   
        semester = Semester.objects.filter(id=pk).prefetch_related('course_set')[0]
    except:
        raise Http404

    scores = Score.objects.filter(course__semester=semester).prefetch_related('student', 'catm', 'course', 'section_a', 'section_b').order_by('student__student_id', 'course__course_code')
    # # exam_marks = ExamMark.objects.filter(course=course)
    # print(scores)

    # data = {c_title: list(items) for c_title, items in  groupby(scores, itemgetter('student_id'))}
    # print(data)
    # queryset = CitiesTable.objects.order_by('country', 'region_or_state')

    scores_dict = {}

    for student, group in groupby(scores, lambda x: x.student):
        scores_dict[student] = {}
        for course, inner_group in groupby(group, lambda x: x.course):
            scores_dict[student][course.course_code] = list(inner_group)

    print(scores_dict)
    return render(request, 'semester_details.html', {"semester": semester, "scores": scores_dict})

def academic_year(request):
    if request.method == "GET":
        academic_years = AcademicYear.objects.all()

        return render(request, 'academic_years.html', {
            'academic_years': academic_years,
            })

    elif request.method == "POST":
        academic_year = AcademicYearForm(request.POST)
        if academic_year.is_valid():
            academic_year.save()
            messages.success(request, "Successfully Updated academic_year Info")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)
       
        else:
            messages.error(request, "Failed To Update academic_year Info")
            err_msg = ""
            for field, errors in academic_year.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)

@login_required()   
def edit_academic_year(request, pk):
    academic_year = get_object_or_404(AcademicYear, id=pk)
    if request.method == "GET":

        return render(request, 'form/academic_year_form.html', {
            "action": reverse('edit_academic_year', args=[pk]),
            'academic_year': academic_year
        })

    if request.method == "POST":
        form = AcademicYearForm(request.POST, instance=academic_year)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update Academic Year Details")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    
    if request.method == "DELETE":
        try:
            academic_year.delete()
            
            messages.success(request, "Successfully Deleted")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Update Academic Year Details")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)

def academic_year_details(request, pk):
    academic_year = get_object_or_404(AcademicYear, id=pk)
    semesters = academic_year.semester_set.all()
    
    return render(request, 'academic_year_details.html', {"academic_year": academic_year, "semesters": semesters})

