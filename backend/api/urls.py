from django.urls import path
from . import views

urlpatterns = [
    path('students/all/', views.students_all, name='api_students_all'),
    path('students/<int:id>/', views.student_view, name='api_student_id')
]
