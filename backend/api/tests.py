from django.test import TestCase, Client
from backend import models
from django.urls import reverse

import time
import json


class APITestCase(TestCase):
    def _add_student(self, data):
        student = models.Student.from_json(data)
        student.save()
        self.students.append(student.to_json())

    def setUp(self):
        self.students = []
        self._add_student({
            'name': {
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'patronymic_name': 'Patron',
            },
            'email': 'ivan@ivan.com',
            'telegram_account': '@ivan'
        })
        self._add_student({
            'name': {
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'patronymic_name': 'Patron',
            },
            'email': 'ivan@ivan.com',
            'telegram_account': '@ivan'
        })

    def test_get_all_students(self):
        c = Client()
        response = c.get(reverse('api_students_all'))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['response']
        self.assertCountEqual(self.students, json_response)

    def test_get_student_ok(self):
        c = Client()
        id = self.students[0]['id']
        response = c.get(reverse('api_student_id', kwargs={'id': id}))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['response']
        self.assertEqual(self.students[0], json_response)

    def test_get_student_no_found(self):
        c = Client()
        response = c.get(reverse('api_student_id', kwargs={'id': 1000000}))
        self.assertEqual(response.status_code, 404)

    def test_patch_student_ok(self):
        c = Client()
        # Getting existing user
        id = self.students[0]['id']
        response = c.get(reverse('api_student_id', kwargs={'id': id}))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['response']
        user_data = json_response
        user_data['name']['first_name'] = 'New name'

        # Updating user name
        response = c.patch(reverse('api_student_id', kwargs={'id': id}),
                           content_type='application/json',
                           data=user_data)
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['response']
        self.assertEqual(user_data, json_response)

        # Getting user again to ensure that the changes were applied
        response = c.get(reverse('api_student_id', kwargs={'id': id}))
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content)['response']
        self.assertEqual(user_data, json_response)
