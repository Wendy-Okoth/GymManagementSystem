from django.urls import path
from . import views

app_name = "members"   # ✅ namespace

urlpatterns = [
    path("", views.member_list, name="list"),
    path("<int:id>/", views.member_detail, name="detail"),
]
