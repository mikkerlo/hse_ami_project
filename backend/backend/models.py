"""
This module contains all models of the project.

See each class docstring to more details
"""

from django.db import models
from django.db.models import Model
from django.conf import settings
from django.dispatch import receiver
from backend import storage

import time
import secrets
import os


class Student(Model):
    """
    This class represents the user of our system.

    Fields:
        first_name       (string):   First name of person
        last_name        (string):   Last name of person
        patronymic_name  (string):   Partonymic name of person
        email            (string):   Email of person at edu.hse.ru domain
        telegram_account (string):   Telegram login, with @ sign: "@john_smith"
        completed homeworks (Many to Many): all homeworks completed by user
        auth_user (One to One): User model corresponding to the student
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    patronymic_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    telegram_account = models.CharField(max_length=255, blank=True)
    completed_homeworks = models.ManyToManyField('Homework')
    auth_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

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
            'telegram_account': self.telegram_account,
            'username': self.auth_user.username,
        }

    def apply_json(self, data):
        if 'name' in data:
            name_data = data['name']
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
        invite_token (string): Invite token for students to join
        students      (Student): Ids of students that are linked to this group
    """
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_hidden = models.BooleanField()
    students = models.ManyToManyField(Student, through='GroupPermission')
    invite_token = models.CharField(
        max_length=256, null=True, default=None, db_index=True)

    def generate_invite_token(self):
        self.invite_token = secrets.token_urlsafe(64)

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


class GroupPermission(Model):
    """
    This class represents a permission of a student, belonging to group.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    NOT_A_MEMBER = -1
    STUDENT = 0
    MODERATOR = 1
    CREATOR = 2

    permission_level = models.IntegerField(default=STUDENT)

    class Meta:
        unique_together = ('group', 'student')


class File(Model):
    """
    This class represents a file that can be attached to a content element.

    Fields:
        name (string): Name of a file, corresponding to a name in file storage
        file (FileField): Actual file.
    """
    name = models.CharField(max_length=4096)
    blob_name = models.CharField(max_length=4096)
    file_url = models.URLField()

    def to_json(self):
        return {
            'id': self.id,
            'url': self.file_url,
            'name': self.name,
        }


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    bucket = storage.get_bucket()
    blob = bucket.blob(instance.blob_name)
    blob.delete()


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
        content_file (file):     Attached media if any are provided

    """
    class Meta:
        abstract = True

    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.BigIntegerField()
    header = models.TextField()
    content = models.TextField(blank=True)
    content_file = models.ManyToManyField(File, blank=True)

    def apply_files(self, data):
        if 'files' not in data:
            return
        files_id = []
        for f in data['files']:
            files_id.append(f['id'])
        files = File.objects.filter(id__in=files_id)
        self.content_file.clear()
        self.content_file.add(*files)

    def apply_json(self, data):
        self.created_at = data['created_at']
        self.header = data['header']
        self.content = data['content']

    def to_json(self):
        files = self.content_file.all()
        files_json = []
        for file in files:
            files_json.append(file.to_json())
        return {
            'id': self.id,
            'group_id': self.group_id.id,
            'group_name': self.group_id.full_name,
            'created_at': self.created_at,
            'header': self.header,
            'content': self.content,
            'files': files_json,
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


class AuthToken(Model):
    """
    This class is an API session token.
    """
    token = models.CharField(max_length=256, unique=True, db_index=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    last_access = models.BigIntegerField()

    @classmethod
    def create_token(cls):
        token = cls()
        token.token = secrets.token_urlsafe(64)
        token.last_access = int(time.time())
        return token

    def validate(self):
        current_time = int(time.time())
        if self.last_access + settings.API_TOKEN_SPOIL >= current_time:
            self.last_access = current_time
            self.save()
            return True
        return False

    def is_expired(self):
        current_time = int(time.time())
        return self.last_access + settings.API_TOKEN_EXPIRE < current_time

    def to_json(self):
        return {
            'token': self.token
        }
