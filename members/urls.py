from django.urls import path
from . import views

app_name = "members"   # ✅ namespace

urlpatterns = [
    # Member list and detail
    path("", views.member_list, name="list"),
    path("<int:id>/", views.member_detail, name="detail"),

    # Member dashboard/session routes
    path("sessions/", views.member_sessions, name="member_sessions"),
    path("api/sessions/", views.member_sessions_api, name="member_sessions_api"),
    path("profile/", views.member_profile, name="member_profile"),
    path("dashboard/", views.member_dashboard, name="member_dashboard"),
]

