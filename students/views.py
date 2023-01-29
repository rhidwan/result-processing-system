from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from students.forms import StudentForm
from itertools import groupby

from students.models import Hall, Student
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def hall(request):
    pass

def hall_detail(request, pk):
    pass

def student(request):

    if request.method == "GET":
        halls = Hall.objects.all()
        students = Student.objects.all()
        
        return render(request, "students.html", {"students": students, "halls":halls})
   
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
def edit_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    if request.method == "GET":
        halls = Hall.objects.all()
        
        return render(request, 'form/student_form.html', {
            "action": reverse('edit_student', args=[pk]),
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
            messages.error(request, "Failed To Update Work Experience")
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
    scores = student.score_set.all()
    semester_dict = {}

    for semester, group in groupby(scores, lambda x: x.course.semester):
        semester_dict[semester] = list(group)
        # for course, inner_group in groupby(group, lambda x: x.course):
        #     semester_dict[semester][course.course_code] = list(inner_group)

    # print(semester_dict)


    return render(request, "student_detail.html", {"student": student, "semesters": semester_dict})

