from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class DocumentStorage(S3Boto3Storage):
    """Storage para documentos en Amazon S3"""
    location = 'documents'
    file_overwrite = False
    default_acl = 'private'
    custom_domain = False