from django.shortcuts import render, redirect
from members.models import Member
from instructors.models import Instructor
from django.contrib.auth import logout 
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render
from .mpesa import initiate_stk_push
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from payments.models import Payment
from django.contrib import messages
from payments.models import Payment
from subscriptions.models import Subscription
import json
import datetime
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

        # Create Django User for authentication
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Member-specific fields
        workout_time = request.POST.get('workout_time')
        specialization = request.POST.get('specialization')
        subscription_plan = request.POST.get('subscription_plan')

        specialization = specialization.title()

        # Assign instructor if available
        instructor_obj = Instructor.objects.filter(
            specialization=specialization,
            gender=gender
        ).first()

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

    return render(request, "signup.html")

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Try Member (Django User)
        user = authenticate(request, username=email, password=password)
        if user is not None and Member.objects.filter(email=email).exists():
            auth_login(request, user)
            return redirect('member_dashboard')

        # Try Instructor (custom model)
        try:
            instructor = Instructor.objects.get(email=email)
            if instructor.check_password(password):
                request.session['instructor_id'] = instructor.id
                return redirect('instructor_dashboard')
            else:
                messages.error(request, "Invalid password")
        except Instructor.DoesNotExist:
            messages.error(request, "Account not found")

        return render(request, "login.html")

    return render(request, "login.html")

def member_dashboard(request):
    return render(request, 'member_dashboard.html')

def member_profile(request):
    return render(request, 'member_profile.html')

def member_payment(request):
    member = Member.objects.get(email=request.user.email)

    plan_amounts = {
        "DAILY": 400,
        "WEEKLY": 1000,
        "MONTHLY": 3000,
        "BIANNUAL": 16000,
        "YEARLY": 30000,
    }

    # Normalize the plan value to uppercase so it matches the dict keys
    plan_key = (member.subscription_plan or "").upper()
    auto_amount = plan_amounts.get(plan_key, 0)

    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        amount = auto_amount

        # Call Daraja API
        response = initiate_stk_push(phone_number, amount)

        # Handle response gracefully
        if response.get("errorCode") == "500.003.02":
            message = "M-Pesa system is busy. Please try again in a few minutes."

        elif response.get("ResponseCode") == "0":
            # ✅ Payment successful
            member.has_paid = True
            member.subscription_expiry = member.calculate_expiry()  # auto-calc expiry
            member.save()

            # Find matching Subscription object
            subscription_obj = Subscription.objects.filter(plan_type=member.subscription_plan).first()

            # Save payment record
            Payment.objects.create(
                member=member,
                subscription=subscription_obj,   # ✅ correct FK
                amount=amount,
                method="MPESA"                   # match choices in Payment model
            )

            message = "Payment successful! Please check your phone to enter your M-Pesa PIN."
            messages.success(request, message)
            return redirect("member_sessions")  # redirect to sessions calendar

        else:
            message = f"Payment failed: {response.get('errorMessage', 'Unknown error')}"
            messages.error(request, message)

        return render(
            request,
            "payment.html",
            {"member": member, "response": message, "auto_amount": auto_amount},
        )

    return render(request, "payment.html", {"member": member, "auto_amount": auto_amount})
    
@login_required
def profile(request):
    member = Member.objects.filter(email=request.user.email).first()
    return render(request, "profile.html", {"member": member})

def logout_view(request):
    logout(request)
    return redirect('home')
