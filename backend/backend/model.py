from django.db import models
from django.db.models import Model


class Student(Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    patronymic_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    email = models.EmailField()
    telegram_account = models.CharField(max_length=255)


class Group(Model):
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)
    description = models.TextField()
    is_hidden = models.BooleanField()
    sudent = models.ManyToManyField(Student)


class File(Model):
    url = models.URLField()
    name = models.CharField(max_length=4096)


class Material(Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    header = models.TextField()
    content = models.TextField()
    content_file = models.ManyToManyField(File)


class Hometask(Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    header = models.TextField()
    content = models.TextField()
    valid_until = models.DateTimeField()
    content_file = models.ManyToManyField(File)


class Notification(Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    header = models.TextField()
    content = models.TextField()
    content_file = models.ManyToManyField(File)


class StudentJar(Model):
    name = models.CharField(max_length=255)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
