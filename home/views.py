from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from datetime import datetime
# Create your views here.

@login_required()
def home(request):
    if request.user.is_staff:
        applications = []
        return render(request, 'index.html')

    else:




        return render(request, 'index.html')

def bkash(request):
    return render(request, 'bkash.html')
