from django.urls import path
from . import deadlines

urls = [
    path('deadlines/all', deadlines.all, name='api_deadlines_all'),
    path('deadlines/<int:id>', deadlines.by_id, name='api_deadliens_view'),
    path('deadlines/new', deadlines.new, name='api_deadlines_new')
]