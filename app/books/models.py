from django.db import models


# Create your models here.
# Upload documents to MEDIA_ROOT/<entry id>/<filename>
# This has to remain here in order for the migrations of books to not break
def upload_path(instance, filename):
    pass
