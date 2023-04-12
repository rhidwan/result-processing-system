from itertools import groupby
import math
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rest_framework import status
from committee.models import AcademicYear, Course, ExamCommittee, Semester
from result.forms import ExamMarkForm, CatmForm
from result.models import Catm, ExamMark, Score
from django.contrib import messages
from result.serializers import ScoreSerializer
from result.utils import render_to_pdf
from django.contrib.auth.decorators import login_required

from students.models import Student
import pandas as pd


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
                
                try:
                    ct_4 = float(data.get('ct_four'+suffix, 0))
                except:
                    ct_4 = 0
          
        
                catm_marks.append([value, attendance, ct_1, ct_2, ct_3, ct_4])
        
        print(catm_marks)
        for av in catm_marks:
            student_id = av[0]
            attendance = av[1]
            ct_1 = av[2]
            ct_2 = av[3]
            ct_3 = av[4]
            ct_4 = av[5]

            student = Student.objects.get(student_id=student_id)

            catm, created = Catm.objects.get_or_create(student=student, attendance=attendance, ct_1=ct_1, ct_2=ct_2, ct_3=ct_3, ct_4=ct_4, course=course)
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
        print(request.POST.get('is_improvement', '0'), type(request.POST.get('is_improvement', '0')))
        is_improvement = True if str(request.POST.get('is_improvement', '0')) == "1" else False

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
            

            exam_mark, created = ExamMark.objects.get_or_create(section=section,code_no=code_no, marks=mark, course=course, is_improvement=is_improvement)
            exam_mark.save()

        messages.success(request, "Successfully Updated Exam Mark")
        return JsonResponse({"status": "success", "msg": "done"}, status=201)

    messages.success(request, "Failed to Update Exam Mark")
    return JsonResponse({"status": "error", "msg": "Something is Wrong"}, status=201)


@login_required()
def edit_exam_mark(request, pk):
    exam_mark = get_object_or_404(ExamMark, id=pk)
    if request.method == "GET":
        return render(request, 'form/single_exam_mark_form.html', {
            "action": reverse('edit_exam_mark', args=[pk]),
            "exam_mark": exam_mark,
        })
    
    if request.method == "POST":
        form = ExamMarkForm(request.POST, instance=exam_mark)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update Exam Mark")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)
    
    if request.method == "DELETE":
        try:
            exam_mark.delete()
            messages.success(request, "Successfully Deleted")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Update Exam mark")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)

@login_required()
def edit_catm(request, pk):
    catm = get_object_or_404(Catm, id=pk)
    
    if request.method == "POST":
        form = CatmForm(request.POST, instance=catm)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)

        else:
            messages.error(request, "Failed To Update Catm")
            err_msg = ""
            for field, errors in form.errors.items():
                for error in errors:
                    err_msg += "\n{} - {}".format(field, error)
            return JsonResponse({"status":"error", "msg": err_msg}, status=200)

def remove_section_from_score(request, pk, section):
    score = get_object_or_404(Score, id=pk)

    if request.method == "DELETE":
        
        try:
            if section == 'a':
                section = score.section_a
                score.section_a = None
                score.save()

            elif section == 'b':
                section = score.section_b
                score.section_b = None
                score.save()
            else:
                return Http404
            section.is_allocated = False
            section.save()

            messages.success(request, "Successfully Removed")
            return JsonResponse({"status": "success", "msg": "Done."}, status=200)
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Update Score")
            return JsonResponse({"status":"error", "msg": "Failed To delete"}, status=200)




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
            score, score_created = Score.objects.get_or_create(course=course, student=student)
            exam_mark = ExamMark.objects.get(course=course, code_no=code_no, section=section)

            # if exam_mark.is_improvement:
            #     if not score.previous_score:
            #         score_data = ScoreSerializer(score)
            #         score.previous_score = score_data.data
            #         score.is_improvement = True

            #Lets change things a bit
            #If the score entry is created, and the score has previous entries Like section A and section B
            #Then it's a new/regular entry. If it has already, then it's an improvement entry
            print(score_created, bool(score.section_a), bool(score.section_b))
            if not score_created and (score.section_a and score.section_b):
                #it's an improvement entry
                print("it's an improvement entry")
                if not score.previous_score:
                    score_data = ScoreSerializer(score)
                    score.previous_score = score_data.data
                    score.is_improvement = True
                    score.section_a = None
                    score.section_b = None
                    
            if section == 'A':
                score.section_a = exam_mark
            elif section == "B":
                score.section_b = exam_mark
            
            exam_mark.is_allocated = True
            exam_mark.save()
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


def generate_tabulation_sheet(request, semester):
    try:   
        semester = Semester.objects.filter(id=semester).prefetch_related('course_set', 'exam_committee')[0]
    except Exception as e:
        print(e)
        raise Http404
    
    try:
        committee = semester.exam_committee.all()[0]
    except:
        committee = None
        
    scores = Score.objects.filter(course__semester=semester).prefetch_related('student', 'catm', 'course', 'section_a', 'section_b').order_by('student__student_id', 'course__course_code')
   
    scores_dict = {}

    for student, group in groupby(scores, lambda x: x.student):
        scores_dict[student] = {}
        for course, inner_group in groupby(group, lambda x: x.course):
            scores_dict[student][course.course_code] = list(inner_group)

    context = {
        "semester": semester, 
        "scores": scores_dict,
        "committee": committee
    }


     # html = template.render(context)
    pdf = render_to_pdf(request, 'pdf/tabulation_sheet.html' , context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "tabulation_sheet_%s.pdf" %( semester.name)
        # content = "inline; filename='%s'" %(filename)
        # download = request.GET.get("download")
        # if download:
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
    
def import_from_excel(request):
    course = request.GET.get('course', None)
    if not course:
        return JsonResponse({"status":"error", "msg": "Course Not Specified"}, status=200)


    if request.method == "POST":            
        course = get_object_or_404(Course, id=course)
        excel = request.FILES['file']
        header = request.POST.get('header_row', 1)
        input_type = request.POST.get('input_type', None)
        if not input_type:
            return JsonResponse({"status":"error", "msg": "Import Type Not Selected"}, status=200)

        
        df = pd.read_excel(excel, header= int(header)-1)
        df.dropna()

        if input_type == "catm":
            student_col = request.POST.get('student_col', "")
            at_mark_col = request.POST.get('at_mark_col', "")
            ct_1_col = request.POST.get('ct_1_mark_col', "")
            ct_2_col = request.POST.get('ct_2_mark_col', "")
            ct_3_col = request.POST.get('ct_3_mark_col', "")
            ct_4_col = request.POST.get('ct_4_mark_col', "")

            if any(x not in df.columns for x in [student_col, at_mark_col, ct_1_col, ct_2_col]):
                print("Columns NOT Found")

                return JsonResponse({"status":"error", "msg": "Specified Columns Not found. Please make sure if the Header row is the correct one"}, status=200)

            catm_marks = []
            for index,row in df.iterrows():
                student_id = str(int(row[student_col]))
                at_mark = row[at_mark_col] 
                ct_1 = row[ct_1_col]
                ct_2 = row[ct_2_col]
                ct_3 = row[ct_3_col]
                if course.credit_point > 2:
                    ct_4 = row[ct_4_col]
                else:
                    ct_4 = 0

                catm_marks.append([student_id, at_mark, ct_1, ct_2, ct_3, ct_4])
            
            for av in catm_marks:
                try:
                    student_id = av[0]
                    attendance = av[1]
                    ct_1 = av[2]
                    ct_2 = av[3]
                    ct_3 = av[4]
                    ct_4 = av[5]

                    if not student_id :
                        continue

                    student, created = Student.objects.get_or_create(student_id=student_id)

                    catm, created = Catm.objects.get_or_create(student=student, attendance=attendance, ct_1=ct_1, ct_2=ct_2, ct_3=ct_3, ct_4=ct_4, course=course)
                    catm.save()

                    score, created = Score.objects.get_or_create(course=course, student=student)

                    score.catm = catm
                    score.save()
                except:
                    import traceback;traceback.print_exc()

            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)


        elif input_type == "exam_mark":
            code_col = request.POST.get('mark_code_col', "")
            mark_col = request.POST.get('mark_mark_col', "")
            print(request.POST.get('mark_section'))
            section = request.POST.get('mark_section', "A").upper()
            
            if any(x not in df.columns for x in [code_col, mark_col]):
                print("Columns NOT Found")
                return JsonResponse({"status":"error", "msg": "Specified Columns Not found. Please make sure if the Header row is the correct one"}, status=200)

            exam_marks = []
            
            for index,row in df.iterrows():
                print(row[code_col], row[mark_col])
                exam_marks.append([row[code_col], row[mark_col]])
            print("Exam Mark,", exam_marks)
            for av in exam_marks:
                code_no = av[0]
                mark = av[1]
                print(code_no, mark, section, "creating")
                
                if pd.isna(code_no) or pd.isna(mark):
                    continue


                exam_mark, created = ExamMark.objects.get_or_create(section=section,code_no=code_no, marks=mark, course=course)
                exam_mark.save()

            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)


            
        elif input_type == "code_mapping":
            code_col = request.POST.get('std_code_col', "")
            std_id_col = request.POST.get('std_id_col', "")
            print(request.POST.get('std_section'))
            section = request.POST.get('std_section', "A").upper()
            
            if any(x not in df.columns for x in [code_col, std_id_col]):
                print("Columns NOT Found")
                return JsonResponse({"status":"error", "msg": "Columns Not found. Please make sure if the Header row or column names are correct!"}, status=200)

            mappings = []
            
            for index,row in df.iterrows():
                print(row[code_col], row[std_id_col])
                try:
                    mappings.append([str(int(row[std_id_col])), row[code_col]])
                except:
                    pass
                    
            for av in mappings:
                student_id = av[0]
                code_no = av[1]
                
                if pd.isna(code_no) or pd.isna(student_id):
                    continue
                # try:
                print(student_id)
                student = Student.objects.get(student_id=student_id)
                # except:
                    # continue
                score, score_created = Score.objects.get_or_create(course=course, student=student)
                exam_mark = ExamMark.objects.get(course=course, code_no=code_no, section=section)

                # if exam_mark.is_improvement:
                #     if not score.previous_score:
                #         score_data = ScoreSerializer(score)
                #         score.previous_score = score_data.data
                #         score.is_improvement = True

                #Lets change things a bit
                #If the score entry is created, and the score has previous entries Like section A and section B
                #Then it's a new/regular entry. If it has already, then it's an improvement entry
                if score_created and not score.section_a and not score.section_b:
                    #it's an improvement entry
                    if not score.previous_score:
                        score_data = ScoreSerializer(score)
                        score.previous_score = score_data.data
                        score.is_improvement = True
                        
                if section == 'A':
                    score.section_a = exam_mark
                elif section == "B":
                    score.section_b = exam_mark
                
                exam_mark.is_allocated = True
                exam_mark.save()
                score.save()
                

            messages.success(request, "Successfully Updated")
            return JsonResponse({"status": "success", "msg": "Done."}, status=201)


        