from django.shortcuts import render
from django.http import HttpResponse

def instructor_list(request):
    return HttpResponse("Instructors list page coming soon!")

def instructor_detail(request, id):
    return HttpResponse(f"Instructor detail page for instructor {id}")

def instructor_dashboard(request):
    return render(request, 'instructor_dashboard.html')

