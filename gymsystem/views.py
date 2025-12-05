from django.shortcuts import render, redirect
from django import forms
from members.models import Member
from instructors.models import Instructor
from django.contrib.auth import logout
from django.shortcuts import redirect


# Signup form
class SignupForm(forms.Form):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('instructor', 'Instructor'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput)

    # Extra fields for instructors
    specialization = forms.CharField(max_length=100, required=False)

    # Extra fields for members
    workout_time = forms.ChoiceField(choices=Member.WORKOUT_TIMES, required=False)


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
        form = SignupForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']

            if role == 'member':
                workout_time = form.cleaned_data['workout_time']
                Member.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    workout_time=workout_time
                )
                return redirect('member_dashboard')

            elif role == 'instructor':
                specialization = form.cleaned_data['specialization']
                Instructor.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    specialization=specialization
                )
                return redirect('instructor_dashboard')
    else:
        form = SignupForm()
    return render(request, "signup.html", {'form': form})

def login(request):
    return render(request, "login.html")

# gymsystem/views.py
def member_dashboard(request):
    return render(request, 'member_dashboard.html')

def member_profile(request):
    return render(request, 'member_profile.html')

def member_sessions(request):
    return render(request, 'member_sessions.html')

def member_payment(request):
    return render(request, 'member_payment.html')

def logout_view(request):
    logout(request)
    return redirect('home')