from itertools import groupby
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from committee.models import AcademicYear, Course, ExamCommittee, Semester
from result.models import Catm, ExamMark, Score
from django.contrib import messages
from result.utils import render_to_pdf

from students.models import Student

# Create your views here.
def catm(request):
    course = request.GET.get('course', None)
    if not course:
        return 

    if request.method == "POST":
        course = get_object_or_404(Course, id=course)
        data = request.POST
        catm_marks = []
        for key, value in data.items():
            if "student_id" in key:
                suffix = key.replace('student_id', "")
                try:
                    attendance = float(data.get('attendance'+suffix, 0))
                except:
                    attendance = 0
                try:
                    ct_1 = float(data.get('ct_one'+suffix, 0))
                except:
                    ct_1 = 0
                try:
                    ct_2 = float(data.get('ct_two'+suffix, 0))
                except:
                    ct_2 = 0
                try:
                    ct_3 = float(data.get('ct_three'+suffix, 0))
                except:
                    ct_3 = 0
          
        
                catm_marks.append([value, attendance, ct_1, ct_2, ct_3])
        
        print(catm_marks)
        for av in catm_marks:
            student_id = av[0]
            attendance = av[1]
            ct_1 = av[2]
            ct_2 = av[3]
            ct_3 = av[4]

            student = Student.objects.get(student_id=student_id)

            catm, created = Catm.objects.get_or_create(student=student, attendance=attendance, ct_1=ct_1, ct_2=ct_2, ct_3=ct_3)
            catm.save()

            score, created = Score.objects.get_or_create(course=course, student=student)

            score.catm = catm
            score.save()
            

        messages.success(request, "Successfully Updated CATM")
        return JsonResponse({"status": "success", "msg": "done"}, status=201)
    if request.method == "DELETE":
        seat = get_object_or_404(Catm, id=course)
        # seat.application_set.all().update(seat=None)
        seat.delete()
        messages.success(request, "Successfully Deleted Seat")
        return JsonResponse({"status": "success", "msg": "done"}, status=201)

    messages.success(request, "Failed to generate seat plan")
    return JsonResponse({"status": "error", "msg": "Something is Wrong"}, status=201)

def catm_detail(request, pk):
    pass

def non_theory_mark(request):
    course = request.GET.get('course', None)
    if not course:
        return 
    
    if request.method == "POST":
        course = get_object_or_404(Course, id=course)
        data = request.POST
       

        exam_marks = []
        for key, value in data.items():
            if "student_id" in key:
                suffix = key.replace('student_id', "")
                try:
                    mark = float(data.get('mark'+suffix, 0))
                except:
                    mark = 0
                
        
                exam_marks.append([value, mark])
        
        print(exam_marks)
        for av in exam_marks:
            student_id = av[0]
            mark = av[1]
            student = Student.objects.get(student_id=student_id)

            score, created = Score.objects.get_or_create(course=course, student=student)

            score.mark_obtained = mark
            score.final_exam_mark = mark
            score.save()
            



        messages.success(request, "Successfully Updated Exam Mark")
        return JsonResponse({"status": "success", "msg": "done"}, status=201)
    if request.method == "DELETE":
        exam_mark = get_object_or_404(ExamMark, id=course)
        # seat.application_set.all().update(seat=None)
        exam_mark.delete()
        messages.success(request, "Successfully Deleted Exam Mark")
        return JsonResponse({"status": "success", "msg": "done"}, status=201)

    messages.success(request, "Failed to Update Exam Mark")
    return JsonResponse({"status": "error", "msg": "Something is Wrong"}, status=201)

def exam_mark(request):
    course = request.GET.get('course', None)
    if not course:
        return 

    if request.method == "POST":
        course = get_object_or_404(Course, id=course)
        data = request.POST
        section = request.POST.get('section', None)
        if not section:
            return

        exam_marks = []
        for key, value in data.items():
            if "code_no" in key:
                suffix = key.replace('code_no', "")
                try:
                    mark = float(data.get('mark'+suffix, 0))
                except:
                    mark = 0
                
        
                exam_marks.append([value, mark])
        
        print(exam_marks)
        for av in exam_marks:
            code_no = av[0]
            mark = av[1]
            

            exam_mark, created = ExamMark.objects.get_or_create(section=section,code_no=code_no, marks=mark, course=course)
            exam_mark.save()



        messages.success(request, "Successfully Updated Exam Mark")
        return JsonResponse({"status": "success", "msg": "done"}, status=201)
    if request.method == "DELETE":
        exam_mark = get_object_or_404(ExamMark, id=course)
        # seat.application_set.all().update(seat=None)
        exam_mark.delete()
        messages.success(request, "Successfully Deleted Exam Mark")
        return JsonResponse({"status": "success", "msg": "done"}, status=201)

    messages.success(request, "Failed to Update Exam Mark")
    return JsonResponse({"status": "error", "msg": "Something is Wrong"}, status=201)

def id_code_mapping(request):
    course = request.GET.get('course', None)
    if not course:
        return 

    if request.method == "POST":
        course = get_object_or_404(Course, id=course)
        data = request.POST
        section = request.POST.get('section', None)
        if not section:
            return

        mappings = []
        for key, value in data.items():
            if "code_no" in key:
                suffix = key.replace('code_no', "")
                try:
                    student_id = data.get('student_id'+suffix, 0)
                except:
                    student_id = 0
                
                print("student_id", student_id)
                mappings.append([ student_id, value])
        
        print(mappings)
        for av in mappings:
            student_id = av[0]
            code_no = av[1]

            # try:
            print(student_id)
            student = Student.objects.get(student_id=student_id)
            # except:
                # continue
            score, created = Score.objects.get_or_create(course=course, student=student)
            exam_mark = ExamMark.objects.get(course=course, code_no=code_no, section=section)
            if section == 'A':
                score.section_a = exam_mark
            elif section == "B":
                score.section_b = exam_mark
            
            score.save()
            
        messages.success(request, "Successfully Updated")
        return JsonResponse({"status": "success", "msg": "done"}, status=201)
    if request.method == "DELETE":
        exam_mark = get_object_or_404(ExamMark, id=course)
        # seat.application_set.all().update(seat=None)
        exam_mark.delete()
        messages.success(request, "Successfully Deleted")
        return JsonResponse({"status": "success", "msg": "done"}, status=201)

    messages.success(request, "Failed to Update")
    return JsonResponse({"status": "error", "msg": "Something is Wrong"}, status=201)


def score(request):
    pass

def score_detail(request, pk):
    pass

def result(request):
    # committee = request.GET.get('committee', None)
    academic_year = request.GET.get('academic_year', AcademicYear.objects.latest().id)
    
    semesters = Semester.objects.filter(academic_year=academic_year)

    return render(request, 'result.html', {"semesters": semesters})

def generate_grade_sheet(request, semester, student_id):
    student = Student.objects.filter(student_id=student_id).prefetch_related('score_set', 'score_set__course', 'score_set__course__semester')
    if not student:
        return HttpResponse(404)
    student = student[0]

    semester = Semester.objects.get(id=semester)
    scores = [x for x in student.score_set.all() if x.course.semester == semester]

    if request.method == "GET":

         # template = get_template('pdf/callback_report.html')
        context = {
             "student": student, 
             "scores": scores, 
             "semester": semester
        }

        # html = template.render(context)
        pdf = render_to_pdf(request, 'pdf/grade_sheet.html' , context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "grade_sheet_%s_%s.pdf" %(student_id, semester.name)
            # content = "inline; filename='%s'" %(filename)
            # download = request.GET.get("download")
            # if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
