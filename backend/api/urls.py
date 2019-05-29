from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.auth_login),
    path('auth/refresh/', views.refresh_token),
    path('auth/change/', views.change_password),

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
    path('groups/<int:group_id>/add-moderator/', views.group_add_moderator,
         name='api_groups_add_moderator'),
    path('groups/<int:group_id>/remove-moderator/',
         views.group_remove_moderator, name='api_groups_remove_moderator'),
    path('groups/<int:group_id>/invite-token/', views.group_invite_token,
         name='api_groups_invite_token'),
    path('groups/invite-token/', views.use_invite_token,
         name='api_use_invite_token'),
    path('groups/new/', views.group_new,
         name='api_groups_new'),

    path('deadlines/<int:deadline_id>/', views.deadline_view,
         name='api_deadlines_id'),
    path('deadlines/<int:deadline_id>/is-done', views.deadline_change_is_done,
         name='api_deadlines_is_done'),
    path('deadlines/new/', views.deadline_new,
         name='api_deadlines_new'),
]
