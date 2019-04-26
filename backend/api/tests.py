from django.test import TestCase, Client
from backend import models
from django.urls import reverse

import json


class APITestCase(TestCase):
    def _add_student(self, data):
        student = models.Student.from_json(data)
        student.save()
        self.students.append(student.to_json())

    def _add_group(self, data, id_list):
        group = models.Group.from_json(data)
        students = list(models.Student.objects.filter(pk__in=id_list))
        group.save()
        group.students.add(*students)
        group.save()
        self.groups.append(group.to_json())

    def _add_homework(self, data, group_id):
        homework = models.Homework.from_json(data)
        homework.group_id = models.Group.objects.get(pk=group_id)
        homework.save()
        self.homeworks.append(homework.to_json())

    def setUp(self):
        self.students = []
        self.groups = []
        self.homeworks = []
        self._add_student({
            'name': {
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'patronymic_name': 'Patron',
            },
            'email': 'ivan@ivan.com',
            'telegram_account': '@ivan',
        })
        self._add_student({
            'name': {
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'patronymic_name': 'Patron',
            },
            'email': 'ivan@ivan.com',
            'telegram_account': '@ivan',
        })

        self._add_group({
            'full_name': 'Group 1',
            'short_name': 'Group 1 short',
            'description': 'Group 1 desc',
            'is_hidden': False,
        }, [self.students[0]['id'], self.students[1]['id']])
        self._add_group({
            'full_name': 'Group 2',
            'short_name': 'Group 2 short',
            'description': 'Group 2 desc',
            'is_hidden': False,
        }, [self.students[1]['id']])

        self._add_homework({
            'created_at': 0,
            'header': 'header 1',
            'content': 'content 1',
            'valid_until': 10,
        }, self.groups[0]['id'])
        self._add_homework({
            'created_at': 0,
            'header': 'header 2',
            'content': 'content 2',
            'valid_until': 10,
        }, self.groups[1]['id'])

    def test_get_all_students(self):
        c = Client()
        response = c.get(reverse('api_students_all'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['result']
        self.assertCountEqual(self.students, json_response)

    def test_get_student_ok(self):
        c = Client()
        student_id = self.students[0]['id']
        response = c.get(
            reverse('api_students_id', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['result']
        self.assertEqual(self.students[0], json_response)

    def test_get_student_no_found(self):
        c = Client()
        response = c.get(
            reverse('api_students_id', kwargs={'student_id': 1000000})
        )
        self.assertEqual(response.status_code, 404)

    def test_patch_student_ok(self):
        c = Client()
        # Getting existing user
        student_id = self.students[0]['id']
        response = c.get(
            reverse('api_students_id', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['result']
        user_data = json_response
        user_data['name']['first_name'] = 'New name'

        # Updating user name
        response = c.patch(
            reverse('api_students_id', kwargs={'student_id': student_id}),
            content_type='application/json',
            data=user_data
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['result']
        self.assertEqual(user_data, json_response)

        # Getting user again to ensure that the changes were applied
        response = c.get(
            reverse('api_students_id', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['result']
        self.assertEqual(user_data, json_response)

    def test_student_new(self):
        c = Client()
        new_student_data = self.students[0]
        new_student_data.pop('id')
        new_student_data['name']['first_name'] = 'Vasa'

        response = c.post(reverse('api_students_new'),
                          content_type='application/json',
                          data=new_student_data)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['result']
        json_response.pop('id')
        self.assertEqual(new_student_data, json_response)

    def test_get_deadlines(self):
        c = Client()
        student_id = self.students[0]['id']

        response = c.get(
            reverse('api_students_deadlines', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['result']
        self.assertCountEqual(json_response, self.homeworks[0:1])

        student_id = self.students[1]['id']
        response = c.get(
            reverse('api_students_deadlines', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['result']
        self.assertCountEqual(json_response, self.homeworks)

    def test_get_groups_one_groups(self):
        c = Client()
        student_id = self.students[0]['id']
        response = c.get(
            reverse('api_students_groups', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['result']
        self.assertCountEqual(json_response, self.groups[0:1])

    def test_get_groups_two_groups(self):
        c = Client()
        student_id = self.students[1]['id']
        response = c.get(
            reverse('api_students_groups', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['result']
        self.assertCountEqual(json_response, self.groups)
