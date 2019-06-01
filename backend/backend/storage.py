from django.conf import settings
from google.cloud import storage

storage_client = storage.Client()


def get_bucket():
    if settings.DEBUG:
        return storage_client.bucket('ami-files-dev')
    else:
        return storage_client.bucket('ami-files')
