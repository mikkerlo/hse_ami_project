from django.test import TestCase
from django.test import Client
from backend import models
from django.urls import reverse
from copy import copy
import json

_STATUS_OK = 200
_STATUS_BAD_REQUEST = 400
_STATUS_NOT_FOUND = 404


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

        self.c = Client()

    # /api/students tests
    def test_student_add_empty_name(self):
        c = Client()

        empty_name = {
            'name': {},
            'email': 'abc@abc.com',
            'telegram_account': '@ivan'
        }

        response = c.post(
            reverse('api_students_new'),
            content_type='application/json',
            data=empty_name
        )

        self.assertEqual(response.status_code, _STATUS_BAD_REQUEST)

    def test_student_add_empty_email(self):
        c = Client()
        no_email = {
            'name': {
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'patronymic_name': 'Ivanovich'
            },
            'telegram_account': '@ivan'
        }

        response = c.post(reverse('api_students_new'),
                          content_type='application/json',
                          data=no_email)

        self.assertEquals(response.status_code, _STATUS_BAD_REQUEST)

        no_email['email'] = None
        response = c.post(reverse('api_students_new'),
                          content_type='application/json',
                          data=no_email)
        self.assertEquals(response.status_code, _STATUS_BAD_REQUEST)

        no_email['email'] = ''
        response = c.post(reverse('api_students_new'),
                          content_type='application/json',
                          data=no_email)
        self.assertEquals(response.status_code, _STATUS_BAD_REQUEST)

    def test_student_add_ok(self):
        c = Client()
        new_student_data = copy(self.students[0])
        new_student_data.pop('id')
        new_student_data['name']['first_name'] = 'Vasa'

        response = c.post(reverse('api_students_new'),
                          content_type='application/json',
                          data=new_student_data)

        self.assertEqual(response.status_code, _STATUS_OK)
        json_response = json.loads(response.content)['result']
        json_response.pop('id')
        self.assertEqual(new_student_data, json_response)

    def test_student_get_all_ok(self):
        c = Client()
        response = c.get(reverse('api_students_all'))
        self.assertEqual(response.status_code, _STATUS_OK)
        json_response = json.loads(response.content)['result']
        self.assertCountEqual(self.students, json_response)
        self.assertListEqual(self.students, json_response)

    def test_student_get_one_ok(self):
        c = Client()
        student_id = self.students[0]['id']
        response = c.get(
            reverse('api_students_id', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, _STATUS_OK)
        json_response = json.loads(response.content)['result']
        self.assertEqual(self.students[0], json_response)

    def test_student_get_one_fail_not_found(self):
        c = Client()
        response = c.get(
            reverse('api_students_id', kwargs={'student_id': 1000000})
        )
        self.assertEqual(response.status_code, 404)

    def test_student_patch_ok(self):
        c = Client()
        # Getting existing user
        student_id = self.students[0]['id']
        response = c.get(
            reverse('api_students_id', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, _STATUS_OK)
        json_response = json.loads(response.content)['result']
        user_data = json_response
        user_data['name']['first_name'] = 'New name'

        # Updating user name
        response = c.patch(
            reverse('api_students_id', kwargs={'student_id': student_id}),
            content_type='application/json',
            data=user_data
        )
        self.assertEqual(response.status_code, _STATUS_OK)
        json_response = json.loads(response.content)['result']
        self.assertEqual(user_data, json_response)

        # Getting user again to ensure that the changes were applied
        response = c.get(
            reverse('api_students_id', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, _STATUS_OK)
        json_response = json.loads(response.content)['result']
        self.assertEqual(user_data, json_response)

    def test_student_patch_fail_empty(self):
        c = Client()

        student_id = self.students[0]['id']

        response = c.patch(
            reverse('api_students_id', kwargs={'student_id': student_id}),
            content_type='application/json',
            data={}
        )
        self.assertEqual(response.status_code, _STATUS_BAD_REQUEST)

        response = c.get(reverse('api_students_id', kwargs={'student_id': student_id}))
        self.assertEqual(response.status_code, _STATUS_OK)
        json_result = json.loads(response.content)['result']
        self.assertEqual(json_result, self.students[0])

    def test_student_patch_fail_illegal_name(self):
        c = Client()

        student_id = self.students[0]['id']

        response = c.get(reverse('api_students_id', kwargs={'student_id': student_id}))

        self.assertEqual(response.status_code, _STATUS_OK)
        student_data = copy(json.loads(response.content)['result'])

        student_data['name'] = {}
        response = c.patch(
            reverse('api_students_id', kwargs={'student_id': student_id}),
            content_type='application/json',
            data=student_data
        )
        self.assertEqual(response.status_code, _STATUS_BAD_REQUEST)
        response = c.get(reverse('api_students_id', kwargs={'student_id': student_id}))
        self.assertEqual(response.status_code, _STATUS_OK)
        json_result = json.loads(response.content)['result']
        self.assertEqual(json_result, self.students[0])

    def test_student_patch_fail_illegal_email(self):
        c = Client()

        student_id = self.students[0]['id']

        response = c.get(reverse('api_students_id', kwargs={'student_id': student_id}))

        self.assertEqual(response.status_code, _STATUS_OK)
        student_data = copy(json.loads(response.content)['result'])

        student_data['email'] = 'abc'
        response = c.patch(
            reverse('api_students_id', kwargs={'student_id': student_id}),
            content_type='application/json',
            data=student_data
        )
        self.assertEqual(response.status_code, _STATUS_BAD_REQUEST)
        response = c.get(reverse('api_students_id', kwargs={'student_id': student_id}))
        self.assertEqual(response.status_code, _STATUS_OK)
        json_result = json.loads(response.content)['result']
        self.assertEqual(json_result, self.students[0])

    def test_student_get_deadlines_ok(self):
        c = Client()
        student_id = self.students[0]['id']

        response = c.get(
            reverse('api_students_deadlines', kwargs={'student_id': student_id})
        )

        self.assertEqual(response.status_code, _STATUS_OK)
        self.assertEqual(json.loads(response.content)['result'][0], self.homeworks[0])

    def test_student_get_deadlines_fail_student_not_found(self):
        c = Client()
        student_id = 100000000
        resp = c.get(
            reverse('api_students_deadlines', kwargs={'student_id': student_id})
        )

        self.assertEqual(resp.status_code, _STATUS_NOT_FOUND)

    def test_student_get_deadlines_fail_empty_deadline_list(self):
        c = Client()

        student_id = self.students[2]['id']
        resp = c.get(reverse('api_students_deadlines', kwargs={'student_id': student_id}))

        self.assertEqual(resp.status_code, _STATUS_OK)
        self.assertEquals(json.loads(resp.content)['result'], [])

    def test_student_get_groups_ok(self):
        student_id = self.students[0]['id']
        resp = self.c.get(
            reverse('api_students_groups', kwargs={'student_id': student_id})
        )

        self.assertEquals(resp.status_code, _STATUS_OK)
        self.assertEquals(json.loads(resp.content)['result'][0], self.groups[0])

    def test_student_get_groups_fail_empty_group_list(self):
        student_id = self.students[2]['id']
        resp = self.c.get(
            reverse('api_students_groups', kwargs={'student_id': student_id})
        )

        self.assertEquals(resp.status_code, _STATUS_OK)
        self.assertEquals(json.loads(resp.content)['result'], [])

    # /api/deadlines tests

    def test_deadline_get_ok(self):
        c = Client()
        student_id = self.students[0]['id']

        response = c.get(
            reverse('api_students_deadlines', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, _STATUS_OK)
        json_response = json.loads(response.content)['result']
        self.assertCountEqual(json_response, self.homeworks[0:1])

        student_id = self.students[1]['id']
        response = c.get(
            reverse('api_students_deadlines', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, _STATUS_OK)
        json_response = json.loads(response.content)['result']
        self.assertCountEqual(json_response, self.homeworks)

    # /api/groups tests

    def test_get_groups_one_groups(self):
        c = Client()
        student_id = self.students[0]['id']
        response = c.get(
            reverse('api_students_groups', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, _STATUS_OK)
        json_response = json.loads(response.content)['result']
        self.assertCountEqual(json_response, self.groups[0:1])

    def test_get_groups_two_groups(self):
        c = Client()
        student_id = self.students[1]['id']
        response = c.get(
            reverse('api_students_groups', kwargs={'student_id': student_id})
        )
        self.assertEqual(response.status_code, _STATUS_OK)
        json_response = json.loads(response.content)['result']
        self.assertCountEqual(json_response, self.groups)
