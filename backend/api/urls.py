from django.urls import path
from . import views

urlpatterns = [
    path('students/all/', views.students_all, name='api_students_all'),
    path('students/<int:id>/', views.student_view, name='api_students_id'),
    path('students/new', views.student_new, name='api_students_new'),
    path('students/<int:id>/deadlines', views.student_deadlines, name='api_students_deadlines'),
    path('students/<int:id>/groups', views.student_groups, name='api_students_groups'),

    path('groups/all/', views.groups_all, name='api_groups_all'),
    path('groups/<int:id>/', views.group_view, name='api_groups_id'),
    path('groups/<int:id>/deadlines/', views.group_deadlines, name='api_groups_deadlines'),
    path('groups/<int:id>/students/', views.group_students, name='api_groups_students'),
    path('groups/new/', views.group_new, name='api_groups_new'),

    path('deadlines/all/', views.deadlines_all, name='api_deadlines_all'),
    path('deadlines/<int:id>/', views.deadline_view, name='api_deadlines_id'),
    path('deadlines/new/', views.deadline_new, name='api_deadlines_new'),
]
