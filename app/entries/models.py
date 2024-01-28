import datetime

from django.db import models

from app.settings import upload_path


# Create your models here.
class Entry(models.Model):
    journal = models.ForeignKey("journals.Journal", on_delete=models.PROTECT, blank=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return str(self.pk)


class EntryRow(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, blank=False)
    date = models.DateField(blank=False, default=datetime.date.today)
    ledger = models.ForeignKey("ledgers.Ledger", on_delete=models.PROTECT, blank=False)
    account = models.ForeignKey("accounts.Account", on_delete=models.PROTECT, null=True, blank=True)
    document = models.FileField(upload_to=upload_path, blank=True)
    value = models.DecimalField(max_digits=99, decimal_places=2, blank=False)

    def __str__(self):
        return str(self.pk)
