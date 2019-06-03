from django.conf import settings
from google.cloud import storage

storage_client = None


def get_bucket():
    global storage_client
    if storage_client is None:
        storage_client = storage.Client()
    if settings.DEBUG:
        return storage_client.bucket('ami-files-dev')
    else:
        return storage_client.bucket('ami-files')
