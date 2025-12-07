from django.shortcuts import render, redirect
from members.models import Member
from instructors.models import Instructor
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render
from .mpesa import initiate_stk_push


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def testimonials(request):
    return render(request, "testimonials.html")

def contact(request):
    return render(request, "contact.html")

def signup(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, "signup.html", {'error': 'Passwords do not match'})

        # Create Django User
        user = User.objects.create_user(
            username=email,   # use email as username
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create Member or Instructor profile
        if role == 'member':
            workout_time = request.POST.get('workout_time')
            Member.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                workout_time=workout_time
            )
            auth_login(request, user)
            return redirect('member_dashboard')

        elif role == 'instructor':
            specialization = request.POST.get('specialization')
            Instructor.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                specialization=specialization
            )
            auth_login(request, user)
            return redirect('instructor_dashboard')

    return render(request, "signup.html")

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect based on role
            if Member.objects.filter(email=email).exists():
                return redirect('member_dashboard')
            elif Instructor.objects.filter(email=email).exists():
                return redirect('instructor_dashboard')
        else:
            return render(request, "login.html", {'error': 'Invalid credentials'})
    return render(request, "login.html")

def member_dashboard(request):
    return render(request, 'member_dashboard.html')

def member_profile(request):
    return render(request, 'member_profile.html')

def member_sessions(request):
    return render(request, 'member_sessions.html')

def member_payment(request):
    return render(request, 'payment.html')

def member_payment(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        amount = request.POST.get("amount")
        response = initiate_stk_push(phone_number, amount)
        return render(request, "payment.html", {"response": response})
    return render(request, "payment.html")


def logout_view(request):
    logout(request)
    return redirect('home')
