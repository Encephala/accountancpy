from django.db import models


# Create your models here.
class Ledger(models.Model):

    id = models.CharField(max_length = 16, primary_key = True, blank = False) # Search name
    name = models.CharField(max_length = 50, blank = False) # Display name
    type = models.CharField(max_length = 3, blank = False,
        choices = [
            ("INC", "Income"),
            ("EXP", "Expenses"),
            ("ASS", "Assets"),
            ("EQU", "Equity"),
            ("LIA", "Liabilities"),
        ]
    )
    notes = models.TextField(blank = True)


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


class Entry(models.Model):
    
    journal = models.ForeignKey(Journal, on_delete = models.PROTECT, blank = False)
    notes = models.TextField(blank = True)

    # TODO: Validation that Entry is balanced


# Upload documents to MEDIA_ROOT/<entry id>/<filename>
def upload_path(instance, filename):
    return f"{instance.entry.id}/{filename}"

class EntryRow(models.Model):

    entry = models.ForeignKey(Entry, on_delete = models.CASCADE, blank = False)
    date = models.DateField(blank = False)
    ledger = models.ForeignKey(Ledger, on_delete = models.PROTECT, blank = False)
    document = models.FileField(upload_to = upload_path, blank = True)
    value = models.DecimalField(max_digits = 99, decimal_places = 2, blank = False)

