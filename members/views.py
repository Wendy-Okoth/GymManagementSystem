from django.shortcuts import render
from django.http import HttpResponse

def member_list(request):
    return HttpResponse("Members list page coming soon!")

def member_detail(request, id):
    return HttpResponse(f"Member detail page for member {id}")

