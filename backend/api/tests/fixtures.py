import pytest
from django.contrib.auth.models import User
import time
from datetime import datetime
from backend.models import Student
from backend.models import Group


def datetime_to_timestamp(year=None, month=None, day=None, hour=None,
                          minute=None, second=None):
    dt = datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second
    )
    return int(time.mktime(dt.timetuple()))


credentials = [
    {
        'username': 'alex',
        'password': 'keksecure3009'
    },
    {
        'username': 'inoc',
        'password': 'keklalsrc234'
    }
]

legal_credentials = credentials

users = [
    {
        'name':             {
            'first_name':      'Алексей',
            'last_name':       'Фигайлов',
            'patronymic_name': ''
        },
        'telegram_account': '@alexfig'
    },
    {
        'name':             {
            'first_name':      'Иннокентий',
            'last_name':       'Епифанцев',
            'patronymic_name': ''
        },
        'telegram_account': '@epiftz'
    },
]

for i in range(len(users)):
    users[i].update(credentials[i])

illegal_users = [
    {
        ''
    },
    {
        'username': 'alex'
    },
    {
        'username': 'alex',
        'password': ''
    },
    {
        'asdkf': 'sdfjk'
    },
    {
        'username':         'alex',
        'telegram_account': '@alexfig'
    },
    {
        'username':         'alex',
        'password':         '123',
        'telegram_account': '@alexfig'
    }
]

groups = [
    {
        'id':          2,
        "full_name":   "Дискретная оптимизация",
        "short_name":  "ДО",
        "description": "Курс читается для студентов 3-го курса ПМИ ФКН ВШЭ в "
                       "4 модуле. Лектор: Игнат Колесниченко. Лекции проходят "
                       "по вторникам, 13:40 - 15:00, ауд. 622, семинары проходят"
                       " сразу после лекции во вторник.",
        "is_hidden":   False
    },
    {
        'id':          3,
        "full_name":   "Алгебра (пилотный поток)",
        "short_name":  "Алгебра (пил)",
        "description": "Алгебра, лектор И. Аржанцев",
        "is_hidden":   False
    },
    {
        "full_name":   "Основы и методология программирования (основной поток)",
        "short_name":  "ОиМП (осн)",
        "description": "Основы и методология программирования, "
                       "лектор М.С. Густокашин",
        "is_hidden":   False
    }
]

groups_creators = [1, 1, 2]

deadlines = [
    {
        "created_at":  datetime_to_timestamp(2019, 4, 5, 20, 59, 59),
        "header":      "Контест ",
        "content":     "Ссылка на контест: "
                       "https://contest.yandex.ru/contest/12792",
        "valid_until": datetime_to_timestamp(2019, 6, 30, 20, 59, 59)
    },
    {
        "created_at":  datetime_to_timestamp(2019, 4, 15, 20, 59, 59),
        "header":      "Написать SVM-кластеризацию для элементов любой алгебры",
        "content":     "Ссылка в канале",
        "valid_until": datetime_to_timestamp(2019, 5, 30, 20, 59, 59)
    },
    {
        "created_at":  datetime_to_timestamp(2019, 5, 20, 20, 59, 59),
        "header":      "Домашка по сетевому взаимодействию",
        "content":     "Писать только на C++: "
                       "https://contest.yandex.ru/contest/23423",
        "valid_until": datetime_to_timestamp(2019, 5, 30, 20, 59, 59)
    },
]

#
# @pytest.fixture(scope='session')
# def django_db_setup(django_db_setup, django_db_blocker):
#     print('setup)')
#     assert len(users) == len(credentials)
#     with django_db_blocker.unblock():
#         for i in range(len(users)):
#             user = Student.objects.create(**users[i])
#             user.set_password(credentials[i]['password'])
#             users[i]['id'] = user.id
#
#         for i in range(len(groups)):
#             group = Group.objects.create(**groups[i])
#
#     # u_1 = User.objects.create(username=students[0]['username'])
#     # u_1.set_password(students[0]['password'])
#     # u_1.save()
#     #
#     # s_1 = Student.objects.create(
#     #     first_name=students[0]['first_name'],
#     #     last_name=students[0]['last_name'],
#     #     auth_user=u_1
#     # )
#     #
#     # u_2 = User.objects.create(username=students[1]['username'])
#     # u_2.set_password(students[1]['password'])
#     # u_2.save()
#     #
#     # s_2 = Student.objects.create(
#     #     first_name=students[1]['first_name'],
#     #     last_name=students[1]['last_name'],
#     #     auth_user=u_2
#     # )
#     #
#     # g_1 = Group.objects.create(**groups[0])
#     # g_1.students.set([s_1])
#     # g_2 = Group.objects.create(**groups[1])
#     #
#     # h_1 = Homework.objects.create(group_id=g_1, **deadlines[0])
