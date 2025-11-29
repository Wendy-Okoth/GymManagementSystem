from django.urls import path
from . import views

app_name = "instructors"   # ✅ namespace

urlpatterns = [
    path("", views.instructor_list, name="list"),
    path("<int:id>/", views.instructor_detail, name="detail"),
]
