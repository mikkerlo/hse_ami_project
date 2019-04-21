from django.urls import path

from . import views
from .api_providers import deadlines

urlpatterns = [
    path('students/all/', views.students_all, name='api_students_all'),
    path('students/<int:id>/', views.student_view, name='api_students_id'),
    path('students/new', views.student_new, name='api_students_new'),
    path('students/<int:id>/deadlines', views.student_deadlines, name='api_students_deadlines'),
    path('students/<int:id>/groups', views.student_groups, name='api_students_groups')
]

urlpatterns.extend(deadlines.urls)
