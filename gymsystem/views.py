from django.shortcuts import render, redirect
from members.models import Member
from instructors.models import Instructor
from django.contrib.auth import logout 
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render
from .mpesa import initiate_stk_push
from django.contrib.auth.decorators import login_required
import re


def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def testimonials(request):
    return render(request, "testimonials.html")

def contact(request):
    return render(request, "contact.html")

SPECIALIZATION_INSTRUCTORS = {
    "Weightlifting": {"MALE": "Daniel Mumbua", "FEMALE": "Grace Njeri"},
    "Cardiovascular Training": {"MALE": "Karanja Kimani", "FEMALE": "Alice Wambui"},
    "Yoga": {"MALE": "Mwambela Mamba", "FEMALE": "Mary Atieno"},
    "Pilates": {"MALE": "Wilson Jeffrey", "FEMALE": "Jane Akinyi"},
    "High Intensive Interval Training": {"MALE": "Maina Mwangi", "FEMALE": "Lucy Chebet"},
    "Functional Training": {"MALE": "Kevin Otieno", "FEMALE": "Sarah Nyambura"},
    "Group Fitness Classes": {"MALE": "Christian Chacha", "FEMALE": "Esther Wanjiku"},
    "Bodybuilding": {"MALE": "Erick Wafula", "FEMALE": "Ann Mwende"},
    "Powerlifting": {"MALE": "Ezekiel Kuria", "FEMALE": "Joyce Achieng"},
    "Flexibility": {"MALE": "Simon Mungai", "FEMALE": "Catherine Wairimu"},
    "Zumba": {"MALE": "Fred Omondi", "FEMALE": "Beatrice Naliaka"},
}

def signup(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        strong_password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$')

        if password != confirm_password:
            return render(request, "signup.html", {'error': 'Passwords do not match.'})

        if not strong_password_regex.match(password):
            return render(request, "signup.html", {
                'error': 'Password must be at least 8 characters long, include uppercase, lowercase, a number, and a special character.'
            })

        # Create Django User
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        if role == 'member':
            workout_time = request.POST.get('workout_time')
            specialization = request.POST.get('specialization')
            subscription_plan = request.POST.get('subscription_plan')

            specialization = specialization.title()

            # Assign instructor based on specialization + gender
            instructor_name = SPECIALIZATION_INSTRUCTORS.get(specialization, {}).get(gender, None)
            instructor_obj = None
            if instructor_name:
                instructor_obj, _ = Instructor.objects.get_or_create(
                    first_name=instructor_name.split()[0],
                    last_name=" ".join(instructor_name.split()[1:]),
                    specialization=specialization,
                    gender=gender
                )

            Member.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                workout_time=workout_time,
                gender=gender,
                specialization=specialization,
                gym_instructor=instructor_obj,
                subscription_plan=subscription_plan,
                has_paid=False
            )
            auth_login(request, user)
            return redirect('member_dashboard')

        elif role == 'instructor':
            specialization = request.POST.get('specialization')
            specialization = specialization.title()
            Instructor.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                specialization=specialization,
                gender=gender
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

@login_required
def profile(request):
    member = Member.objects.filter(email=request.user.email).first()
    return render(request, "profile.html", {"member": member})

def logout_view(request):
    logout(request)
    return redirect('home')
