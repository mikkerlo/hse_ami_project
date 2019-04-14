from django.urls import path
from . import views

urlpatterns = [
    path('students/all/', views.students_all),
    path('students/<int:id>/', views.student_view)
]
