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

    def __str__(self):
        return self.id
