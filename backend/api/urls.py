from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.auth_login),
    path('auth/refresh/', views.refresh_token),
    path('auth/change', views.change_password),

    path('file/upload/', views.upload_file),

    path('students/all/', views.students_all,
         name='api_students_all'),
    path('students/student/', views.student_view,
         name='api_students_id'),
    path('students/new/', views.student_new,
         name='api_students_new'),
    path('students/deadlines/', views.student_deadlines,
         name='api_students_deadlines'),
    path('students/groups/', views.student_groups,
         name='api_students_groups'),

    path('groups/all/', views.groups_all,
         name='api_groups_all'),
    path('groups/<int:group_id>/', views.group_view,
         name='api_groups_id'),
    path('groups/<int:group_id>/deadlines/', views.group_deadlines,
         name='api_groups_deadlines'),
    path('groups/<int:group_id>/students/', views.group_students,
         name='api_groups_students'),
    path('groups/new/', views.group_new,
         name='api_groups_new'),

    path('deadlines/all/', views.deadlines_all,
         name='api_deadlines_all'),
    path('deadlines/<int:deadline_id>/', views.deadline_view,
         name='api_deadlines_id'),
    path('deadlines/new/', views.deadline_new,
         name='api_deadlines_new'),
]
