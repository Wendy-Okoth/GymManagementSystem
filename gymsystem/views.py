from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def testimonials(request):
    return render(request, "testimonials.html")

def contact(request):
    return render(request, "contact.html")

def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")