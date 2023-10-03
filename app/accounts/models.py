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

    def __str__(self):
        return self.id
