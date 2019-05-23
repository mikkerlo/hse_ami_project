import pytest
from django.contrib.auth.models import User

from backend.models import Student

auth_user = {
    'username': 'nikita',
    'password': '123'
}
student = {
    'first_name': 'Nikita',
    'last_name': 'Orlov'
}

students = [
    {
        'username': 'test_1',
        'password': '123',
        'first_name': 'Test1FirstName',
        'last_name': 'Test1LastName'
    },
    {
        'username': 'test_2',
        'password': '123',
        'first_name': 'Test2FirstName',
        'last_name': 'Test2LastName'
    }
]

groups = [
    {
        'full_name': 'test_1_full_name',
        'short_name': 'test_1',
        'is_hidden': False
    },
    {
        'full_name': 'test_2_full_name',
        'short_name': 'test_2',
        'is_hidden': False
    }
]

deadlines = [
    {
        'created_at': 0,
        'header': 'test_1_deadline',
        'valid_until': 1
    }
]
