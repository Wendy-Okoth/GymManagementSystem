from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_list, name='feedback_list'),
    path('new/', views.feedback_create, name='feedback_create'),
    path('<int:pk>/edit/', views.feedback_edit, name='feedback_edit'),
    path('<int:pk>/delete/', views.feedback_delete, name='feedback_delete'),
]
