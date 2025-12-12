
from django.contrib import admin
from django.urls import path , include
from . import views
from gymsystem import views as system_views
from members import views as member_views
from instructors import views as instructor_views
from payments.views import mpesa_callback

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("members/", include("members.urls", namespace="members")),
    path("subscriptions/", include("subscriptions.urls", namespace="subscriptions")),
    path("payments/", include("payments.urls", namespace="payments")),
    path("attendance/", include("attendance.urls", namespace="attendance")),
    path("instructors/", include("instructors.urls", namespace="instructors")),
    path("about/", views.about, name="about"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("contact/", views.contact, name="contact"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path('signup/', system_views.signup, name='signup'),
    path('member/dashboard/', member_views.member_dashboard, name='member_dashboard'),
    path('instructor/dashboard/', instructor_views.instructor_dashboard, name='instructor_dashboard'),
    path("profile/", views.profile, name="profile"),
    path('dashboard/', views.member_dashboard, name='member_dashboard'),
    path('profile/', views.member_profile, name='member_profile'),
    path('sessions/', views.member_sessions, name='member_sessions'),
    path('payment/', views.member_payment, name='member_payment'),
    path("mpesa/callback/", mpesa_callback, name="mpesa_callback"),
    path('logout/', views.logout_view, name='logout'),
]


