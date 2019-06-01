# Generated by Django 2.1.7 on 2019-06-01 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_group_invite_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='file',
        ),
        migrations.AddField(
            model_name='file',
            name='blob_name',
            field=models.CharField(default='nothing.txt', max_length=4096),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='file_url',
            field=models.URLField(default='https://storage.cloud.google.com/ami-files/kek'),
            preserve_default=False,
        ),
    ]
