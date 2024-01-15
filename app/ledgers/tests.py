from django.test import TestCase
from django.urls import reverse

from .models import Ledger

# Create your tests here.
class LedgersViewsTest(TestCase):

    # Create ledger and see if it's in the rendered list
    def test_ledger_details(self):
        l1 = Ledger("test", "a testing ledger", "ASS")
        l1.full_clean()
        l1.save()

        response = self.client.get(reverse("ledgers:details", args = [l1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, l1.name)


    def test_ledger_list_populated(self):
        names = ["A testing ledger", "A second one"]
        l1 = Ledger("ledger 1", names[0], "ASS")
        l2 = Ledger("ledger 2", names[1], "INC")

        l1.full_clean()
        l2.full_clean() # hehe this is bad code
        l1.save()
        l2.save()

        response = self.client.get(reverse("ledgers:hx-list"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["ledger_list"],
            [l1, l2],
            ordered = False
        )
