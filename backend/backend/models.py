"""
Description of objects we will operate with.

Student is a person, described by its credentials. Group is a set of Students that attends to a
specific learning course, where this course is unique for every group. Content element is an
information that is important for a specific group.
"""

from django.db import models
from django.db.models import Model


class Student(Model):
    """
    Student description class. Holds basic information about our system user.

    Fields:
        first_name       (string):   First name of person
        last_name        (string):   Last name of person
        patronymic_name  (string):   Partonymic name of person
        birth_date       (datetime): Date of birth of a student
        email            (string):   Email of person at edu.hse.ru domain
        telegram_account (string):   Telegram login, with @ sign, for example: "@john_smith"
    """
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    patronymic_name = models.CharField(max_length=255, blank=False, null=True)
    birth_date = models.DateField(blank=False, null=False)
    email = models.EmailField(blank=True, null=False)
    telegram_account = models.CharField(max_length=255, blank=False, null=True)


class Group(Model):
    """
    Group description class. Holds basic information about user groups.
    
    Fields:
        full_name   (string):  Group full name, is shown in group description page     
        short_name  (string):  Group short name, is used to search group in database
        description (string):  Group description, arbitrary text, providen by group creator
        is_hidden   (bool):    Flag, if is true, group is not shown on search result page
        sudent      (Student): Ids of students that are linked to this group
    
    """
    full_name = models.CharField(max_length=255, blank=False, null=False)
    short_name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(null=True)
    is_hidden = models.BooleanField(null=False)
    sudent = models.ManyToManyField(Student)


class File(Model):
    """
    Infromation about uploaded files into system.

    Fields:
        url  (string): URL of file, starting at root of server, for example,
        '/<api_endpoint>/example.txt'
        name (string): Name of such a file
    """
    url = models.URLField(blank=False, null=False)
    name = models.CharField(max_length=4096, blank=False, null=False)


class ContentElement(Model):
    """
    Base class for three main content elements of system: Notifications, Materials and Hometasks.

    Fields:
        group_id     (id):       id of group for which the element is linked
        created_at   (datetime): Moment of time when the element is created
        header       (string):   Header or title of element
        content      (string):   Main content of elmeent
        content_file (file):     Attached files, if any are providen

    """
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(blank=False, null=False)
    header = models.TextField(blank=False, null=False)
    content = models.TextField(blank=True, null=False)
    content_file = models.ManyToManyField(File, blank=False, null=True)

    class Base:
        abstract = True


class Material(ContentElement):
    """
    Material specialization of ContentElement class
    """
    pass


class Hometask(ContentElement):
    """
    Hometask specialization of ContentElement class. Contains additional field for holding
    deadline time.

    Fields:
        valid_until (datetime): Moment in time after which task is no longer relevant.

    """
    valid_until = models.DateTimeField()


class Notification(ContentElement):
    """
    Notification specialization of ContentElement class.
    """
    pass


class StudentJar(Model):
    """
    Class for jar of students. Used to store lists of students for ease of navigation and group
    manipulation. Can be created by any user in system.

    Fields:
        name (string): Name of student jar, used in search. Must be unique.
        created_by (student id): Id of student that created this jar.
        student_id (student id): Id of students that are linked to this jar.
    """
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(Student)
    student_id = models.ManyToManyField(Student, on_delete=models.CASCADE)
