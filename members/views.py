from django.shortcuts import render
from django.http import HttpResponse

def member_list(request):
    return HttpResponse("Members list page coming soon!")

def member_detail(request, id):
    return HttpResponse(f"Member detail page for member {id}")

def member_dashboard(request):
    return render(request, 'member_dashboard.html')

def member_dashboard(request):
    return render(request, 'member_dashboard.html')

def member_profile(request):
    return render(request, 'member_profile.html')

def member_sessions(request):
    return render(request, 'member_sessions.html')

def member_payment(request):
    return render(request, 'member_payment.html')
