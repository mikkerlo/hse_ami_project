"""
This module contains all models of the project.

See each class docstring to more details
"""

from django.db import models
from django.db.models import Model


class Student(Model):
    """
    This class represents the user of our system.

    Fields:
        first_name       (string):   First name of person
        last_name        (string):   Last name of person
        patronymic_name  (string):   Partonymic name of person
        birth_date       (datetime): Date of birth of a student
        email            (string):   Email of person at edu.hse.ru domain
        telegram_account (string):   Telegram login, with @ sign, for example: "@john_smith"
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    patronymic_name = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField()
    email = models.EmailField(blank=True)
    telegram_account = models.CharField(max_length=255, blank=True)
    done_homeworks = models.ManyToManyField('Homework')


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
        short_name  (string):  Group short name, гsed to search group in database
        description (string):  Group description, arbitrary text provided by group creator
        is_hidden   (bool):    Flag, if is true group is not shown on search result page
        students      (Student): Ids of students that are linked to this group
    
    """
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_hidden = models.BooleanField()
    students = models.ManyToManyField(Student)


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
    Base class for three main content elements of system: Notifications, Materials and Homeworks.

    This class represents an information entry that may be created in a group
    to be displayed to its students.

    Fields:
        group_id     (id):       Id of element's group.
        created_at   (datetime): Creation timestamp
        header       (string):   Header of element
        content      (string):   Main content of element
        content_file (file):     Attached files if any are provided

    """
    class Meta:
        abstract = True

    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    header = models.TextField()
    content = models.TextField(blank=True)
    content_file = models.ManyToManyField(File, blank=True)


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
    valid_until = models.DateTimeField()


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
    created_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)
