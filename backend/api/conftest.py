import pytest
from django.contrib.auth.models import User

from backend.models import Student, Group, Homework
from tests.fixtures import auth_user, student
from tests.fixtures import students, groups, deadlines


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    print('Setup')
    with django_db_blocker.unblock():
        u_1 = User.objects.create(username=students[0]['username'])
        u_1.set_password(students[0]['password'])
        u_1.save()

        s_1 = Student.objects.create(
            first_name=students[0]['first_name'],
            last_name=students[0]['last_name'],
            auth_user=u_1
        )

        u_2 = User.objects.create(username=students[1]['username'])
        u_2.set_password(students[1]['password'])
        u_2.save()

        s_2 = Student.objects.create(
            first_name=students[1]['first_name'],
            last_name=students[1]['last_name'],
            auth_user=u_2
        )

        g_1 = Group.objects.create(**groups[0])
        g_1.students.set([s_1])
        g_2 = Group.objects.create(**groups[1])

        h_1 = Homework.objects.create(group_id=g_1, **deadlines[0])

