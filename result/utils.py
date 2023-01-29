from io import BytesIO
import json
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os
# from xhtml2pdf import pisa
from weasyprint import HTML, CSS
import zipfile

# from PyPDF2 import PdfFileMerger

def link_callback(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.PDF_STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/
    print("I am here")
    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
        print(path)
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri
    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' % (sUrl, mUrl))
    return path


def render_to_pdf(request, template_src, context_dict={} ):
    template = get_template(template_src)

    html  = template.render(context_dict)

    base_url = os.path.dirname(os.path.realpath(__file__))
    pdf_file = HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf()

    # result = BytesIO()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'
    return response

def render_pdf(request, template_src, context_dict={} ):
    template = get_template(template_src)

    html  = template.render(context_dict)

    base_url = os.path.dirname(os.path.realpath(__file__))
    pdf_file = HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf()

    return pdf_file


def generate_zip(files):
    mem_zip = BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])

    return mem_zip.getvalue()

# def merge_pdf(files):
#     mem_pdf = BytesIO()
#     merger = PdfFileMerger()
#     pdf_files = [x for x in files if x.endswith(".pdf")]
#     [merger.append(pdf) for pdf in pdf_files]
    
#     merger.write(mem_pdf)
    
#     return mem_pdf.getvalue()

def get_letter_grade_point(percentage):
    '''
    80% or above A+ 4. 4
    75% to less than 80% A 3.75 4
    70% to less than 75% A- 3.5
    65 to less than 70% B+ 3.25
    60% to less than 65% B 3.0
    55% to less than 60% B- 2.75
    50 to less than 55% C+ 2.5
    45% to less than 50% C 2.25
    40 to less than 45% D 2.0 
    less than 40% F 0.0
    Incomplete I 0.0
    '''

    if percentage >= 80:
        return 'A+' , 4 
    elif percentage < 80 and percentage >= 75:
        return 'A', 3.75
    elif percentage < 75 and percentage >= 70:
        return 'A-', 3.5
    elif percentage < 70 and percentage >= 65:
        return 'B+', 3.25
    elif percentage < 65 and percentage >= 60 :
        return 'B', 3.0
    elif percentage < 60 and percentage >= 55:
        return 'B-', 2.75
    elif percentage < 55 and percentage >= 50:
        return 'C+', 2.50
    elif percentage < 50 and percentage >= 45:
        return 'C', 2.25
    elif percentage < 45 and percentage >= 40:
        return 'D', 2.0
    elif percentage < 40:
        return 'F', 0
