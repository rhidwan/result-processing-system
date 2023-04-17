from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from students.forms import StudentForm, HallForm
from itertools import groupby

from students.models import Hall, Student
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def hall(request):

    if request.method == "GET":
        halls = Hall.objects.all().prefetch_related('student_set')
        return render(request, 'hall.html', {"halls": halls})
    elif request.method == "POST":
        hall = HallForm(request.POST)
        if hall.is_valid():
            hall.save()
            messages.success(request, "Successfully Created Hall Entry")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)
       
        else:
            messages.error(request, "Failed To Create student ")
            err_msg = ""
            for field, errors in hall.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)


def hall_detail(request, pk):
    pass

def edit_hall(request, pk):
    hall = get_object_or_404(Hall, id=pk)
    if request.method == "GET":
        return render(request, 'form/hall_form.html', {
            "action": reverse('edit_hall', args=[pk]),
            "hall": hall, 
        })

    if request.method == "POST":
        form = HallForm(request.POST, instance=hall)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update hall Information")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    
    if request.method == "DELETE":
        try:
            hall.delete()
            
            messages.success(request, "Successfully Deleted")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Update Hall Form")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)



def student(request):

    if request.method == "GET":
        session = request.GET.get('session', None)
        hall = request.GET.get('hall', None)

        query = Q()
        if session:
            query &= Q(session=session)
        if hall:
            query &= Q(hall=hall)


    
        halls = Hall.objects.all()
        sessions = list(Student.objects.order_by('session').values_list('session', flat=True).distinct())
        print(sessions)

        student_list = Student.objects.filter(query).prefetch_related('hall')
        
        page = request.GET.get('page', 1)
        paginator = Paginator(student_list, 20)

        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)

        return render(request, "students.html", {"students": students, "halls":halls, "sessions":sessions, "filters": {"session": session, "hall": hall}})
   
    elif request.method == "POST":
        print(request.POST)
        committee = StudentForm(request.POST)
        if committee.is_valid():
            committee.save()
            messages.success(request, "Successfully Created Student Entry")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)
       
        else:
            messages.error(request, "Failed To Create student ")
            err_msg = ""
            for field, errors in committee.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)


   
@login_required()
def edit_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    if request.method == "GET":
        halls = Hall.objects.all()
        return render(request, 'form/student_form.html', {
            "action": reverse('edit_student', args=[student_id]),
            "student": student,
            "halls": halls, 
        })

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update Student Information")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    
    if request.method == "DELETE":
        try:
            student.delete()
            
            messages.success(request, "Successfully Deleted")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Update Work Experience")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)


def exam_committe_detail(request, pk):

    return render(request, "committee_detail.html")

    

def student_detail(request, student_id):
    student = Student.objects.filter(student_id=student_id).prefetch_related('score_set', 'score_set__course', 'score_set__course__semester')
    if not student:
        return HttpResponse(404)
    student = student[0]

    # semesters = student.score_set.values_list('course__semester').distinct()
    scores = student.score_set.all().order_by('course__semester')
    semester_dict = {}

    for semester, group in groupby(scores, lambda x: x.course.semester):
        semester_dict[semester] = list(group)
        # for course, inner_group in groupby(group, lambda x: x.course):
        #     semester_dict[semester][course.course_code] = list(inner_group)

    # print(semester_dict)


    return render(request, "student_detail.html", {"student": student, "semesters": semester_dict})

