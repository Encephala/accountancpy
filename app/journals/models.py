from django.db import models


# Create your models here.
class Journal(models.Model):
    id = models.CharField(max_length=16, primary_key=True, blank=False)  # noqa: A003 - Search name
    name = models.CharField(max_length=50, blank=False)  # Display name
    type = models.CharField(  # noqa: A003
        max_length=3,
        blank=False,
        choices=[
            ("INC", "Income"),
            ("EXP", "Expense"),
            ("CAS", "Cash"),
            ("GEN", "General"),
        ],
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return str(self.id)
