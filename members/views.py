from django.shortcuts import render
from django.http import HttpResponse
import datetime
from .models import Member

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

def member_payment(request):
    return render(request, 'member_payment.html')

def member_sessions(request):
    member = Member.objects.get(email=request.user.email)

    # ✅ Only show sessions if member has paid AND subscription is active
    if not member.has_paid or not member.is_subscription_active():
        return render(request, "member_sessions.html", {"sessions": []})

    start_date = datetime.date.today() + datetime.timedelta(days=1)
    sessions = []

    # Workout time slots
    workout_slots = {
        "MORNING": "7:00 AM - 10:00 AM",
        "AFTERNOON": "12:00 PM - 3:00 PM",
        "EVENING": "4:00 PM - 7:00 PM",
        "NIGHT": "9:00 PM - 12:00 AM",
    }

    plan = (member.subscription_plan or "").upper()

    def add_sessions(limit_days):
        """Helper to add weekday sessions up to limit_days or until expiry"""
        days_added = 0
        current = start_date
        while days_added < limit_days and (member.subscription_expiry is None or current <= member.subscription_expiry):
            if current.weekday() < 5:  # Monday–Friday only
                sessions.append({
                    "date": current,
                    "day": current.strftime("%A"),
                    "trainer": member.gym_instructor,
                    "time": workout_slots.get(member.workout_time.upper(), "N/A")
                })
                days_added += 1
            current += datetime.timedelta(days=1)

    # Plan logic
    if plan == "DAILY":
        add_sessions(1)
    elif plan == "WEEKLY":
        add_sessions(5)
    elif plan == "MONTHLY":
        add_sessions(28)
    elif plan in ["BIANNUAL", "BI_ANNUAL"]:
        add_sessions(120)   # ~6 months weekdays
    elif plan in ["YEARLY", "ANNUAL"]:
        add_sessions(240)   # ~12 months weekdays

    return render(request, "member_sessions.html", {"sessions": sessions})


