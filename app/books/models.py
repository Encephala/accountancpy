from django.db import models


# Create your models here.
class Account(models.Model):

    id = models.CharField(max_length = 16, primary_key = True, blank = False) # Search name
    name = models.CharField(max_length = 50, blank = False) # Display name
    is_creditor = models.BooleanField(blank = False,
        choices = [
            (False, "Debtor"),
            (True, "Creditor")
        ]
    )
    notes = models.TextField(blank = True)


class Journal(models.Model):

    id = models.CharField(max_length = 16, primary_key = True, blank = False) # Search name
    name = models.CharField(max_length = 50, blank = False) # Display name
    type = models.CharField(max_length = 3, blank = False,
        choices = [
            ("INC", "Income"),
            ("EXP", "Expense"),
            ("CAS", "Cash"),
            ("GEN", "General"),
        ]
    )
    notes = models.TextField(blank = True)

# Upload documents to MEDIA_ROOT/<entry id>/<filename>
# This has to remain here in order for the migrations of books to not break
def upload_path(instance, filename):
    pass
