from django.db import models
from app.settings import upload_path

# Create your models here.
class Entry(models.Model):

    # TODO: Weg van books.Journal en over naar "journal.Journal"
    journal = models.ForeignKey("books.Journal", on_delete = models.PROTECT, blank = False)
    notes = models.TextField(blank = True)

    # TODO: Validation that Entry is balanced


class EntryRow(models.Model):

    entry = models.ForeignKey(Entry, on_delete = models.CASCADE, blank = False)
    date = models.DateField(blank = False)
    ledger = models.ForeignKey("ledgers.Ledger", on_delete = models.PROTECT, blank = False)
    document = models.FileField(upload_to = upload_path, blank = True)
    value = models.DecimalField(max_digits = 99, decimal_places = 2, blank = False)