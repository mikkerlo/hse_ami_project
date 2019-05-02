"""
This module contains all models of the project.

See each class docstring to more details
"""

from django.db import models
from django.db.models import Model
from django.core.validators import validate_email


class Student(Model):
    """
    This class represents the user of our system.

    Fields:
        first_name       (string):   First name of person
        last_name        (string):   Last name of person
        patronymic_name  (string):   Partonymic name of person
        email            (string):   Email of person at edu.hse.ru domain
        telegram_account (string):   Telegram login, with @ sign: "@john_smith"
    """
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    patronymic_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=False)
    telegram_account = models.CharField(max_length=255, blank=True)
    completed_homeworks = models.ManyToManyField('Homework')

    def to_json(self):
        """Transform the object to json dict for api usage"""
        return {
            'id': self.id,
            'name': {
                'first_name': self.first_name,
                'last_name': self.last_name,
                'patronymic_name': self.patronymic_name,
            },
            'email': self.email,
            'telegram_account': self.telegram_account
        }

    def apply_json(self, data):
        if 'name' not in data or \
            'email' not in data:
            raise ValueError('"name" and "email" fields are required')

        if not (data['name'] and data['email']):
            raise ValueError('"name" and "email" fields need to be non-empty')

        name_data = data['name']

        if 'first_name' not in name_data or 'last_name' not in name_data:
            raise ValueError('"first_name" and "last_name" are required')

        if not (name_data['first_name'] and name_data['last_name']):
            raise ValueError('"first_name" and "last_name" fields need to be non-empty')

        validate_email(data['email'])

        self.first_name = name_data.get('first_name', self.first_name)
        self.last_name = name_data.get('last_name', self.last_name)
        self.patronymic_name = name_data.get('patronymic_name',
                                             self.patronymic_name)
        self.email = data.get('email', self.email)
        self.telegram_account = data.get('telegram_account',
                                         self.telegram_account)

    @classmethod
    def from_json(cls, data):
        obj = cls()
        obj.apply_json(data)
        return obj


class Group(Model):
    """
    This class represents a collection of users, attending the same course.

    It is important to highlight, that this class doesn't specify academic
    group, but instead a collection of students attending the same course
    at the same time.
    Therefore, one student can have multiple groups and each course can have
    multiple groups dedicated to it.

    Fields:
        full_name   (string):  Group full name, shown in group description page
        short_name  (string):  Group short name, used to search in database
        description (string):  Group description, provided by group creator
        is_hidden   (bool):    If is true group is not shown on result page
        students      (Student): Ids of students that are linked to this group
    """
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_hidden = models.BooleanField()
    students = models.ManyToManyField(Student)

    def apply_json(self, data):
        self.full_name = data.get('full_name', self.full_name)
        self.short_name = data.get('short_name', self.short_name)
        self.description = data.get('description', self.description)
        self.is_hidden = data.get('is_hidden', self.is_hidden)

    def to_json(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'short_name': self.short_name,
            'description': self.description,
            'is_hidden': self.is_hidden
        }

    @classmethod
    def from_json(cls, data):
        obj = cls()
        obj.apply_json(data)
        return obj


class File(Model):
    """
    This class represents a file that can be attached to a content element.

    Fields:
        url  (string): URL of file, starting at root of server, for example,
        '/<api_endpoint>/example.txt'
        name (string): Name of a file, corresponding to a name in file storage
    """
    url = models.URLField()
    name = models.CharField(max_length=4096)


class ContentElement(Model):
    """
    Base class for three main content elements of system: Notifications,
    Materials and Homeworks.

    This class represents an information entry that may be created in a group
    to be displayed to its students.

    Fields:
        group_id     (id):       Id of element's group.
        created_at   (int): Creation timestamp
        header       (string):   Header of element
        content      (string):   Main content of element
        content_file (file):     Attached files if any are provided

    """
    class Meta:
        abstract = True

    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.BigIntegerField()
    header = models.TextField()
    content = models.TextField(blank=True)
    content_file = models.ManyToManyField(File, blank=True)

    def apply_json(self, data):
        self.created_at = data['created_at']
        self.header = data['header']
        self.content = data['content']

    def to_json(self):
        return {
            'id': self.id,
            'group_id': self.group_id.id,
            'group_name': self.group_id.full_name,
            'created_at': self.created_at,
            'header': self.header,
            'content': self.content,
        }


class Material(ContentElement):
    """
    This class represents some useful material relevant to the course.
    """
    pass


class Homework(ContentElement):
    """
    This class represents a given task with a set deadline.

    Fields:
        valid_until (datetime): Deadline expiration absolute timestamp.

    """
    valid_until = models.BigIntegerField()

    def apply_json(self, data):
        super().apply_json(data)
        self.valid_until = data.get('valid_until', self.valid_until)

    def to_json(self):
        result = super().to_json()
        result['valid_until'] = self.valid_until
        return result

    @classmethod
    def from_json(cls, data):
        obj = cls()
        obj.apply_json(data)
        return obj


class Notification(ContentElement):
    """
    This class represents an important announcement about the course.
    """
    pass


class StudentJar(Model):
    """
    This class stores list of students for ease of navigation and group
    manipulation. Can be created by any user in system.

    Fields:
        name (string): Name of student jar, used in search.
        created_by (student id): Id of student that created this jar.
        students (student id): Id of students that are linked to this jar.
    """
    name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(Student, on_delete=models.CASCADE,
                                   related_name='student_jars_created')
    students = models.ManyToManyField(Student)
