from django.db import models


# Create your models here.
class Ledger(models.Model):

    id = models.CharField(max_length = 16, primary_key = True) # Search name
    name = models.CharField(max_length = 50) # Display name
    type = models.CharField(max_length = 3,
        choices = [
            ("INC", "Income"),
            ("EXP", "Expenses"),
            ("ASS", "Assets"),
            ("EQU", "Equity"),
            ("LIA", "Liabilities")
        ]
    )
    notes = models.TextField()


class Account(models.Model):

    id = models.CharField(max_length = 16, primary_key = True) # Search name
    name = models.CharField(max_length = 50) # Display name
    is_creditor = models.BooleanField(
        choices = [
            (False, "Debtor"),
            (True, "Creditor")
        ]
    )
    notes = models.TextField()


class Entries(models.Model):
    
    notes = models.TextField()


# Upload documents to MEDIA_ROOT/<entry id>/<filename>
def upload_path(instance, filename):
    return f"{instance.entry.id}/{filename}"

class EntriesRow(models.Model):

    entry = models.ForeignKey(Entries, on_delete = models.CASCADE)
    date = models.DateField()
    ledger = models.ForeignKey(Ledger, on_delete = models.PROTECT)
    document = models.FileField(upload_to = upload_path)
    value = models.DecimalField(decimal_places = 2)

