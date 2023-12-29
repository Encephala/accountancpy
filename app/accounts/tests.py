from django.test import TestCase
from django.urls import reverse

from .models import *

# Create your tests here.
class AccountsViewsTest(TestCase):

    # Create account and see if it's in the rendered list
    def test_account_overview(self):
        response = self.client.get(reverse("accounts:overview"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Overview of Accounts")


    def test_account_details(self):
        l1 = Account("test", "a testing Account", True)
        l1.full_clean()
        l1.save()

        response = self.client.get(reverse("accounts:details", args = [l1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, l1.name)


    def test_account_list_empty(self):
        response = self.client.get(reverse("accounts:hx-list"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["account_list"],
            []
        )

    def test_account_list_populated(self):
        names = ["A testing Account", "A second one"]
        l1 = Account("Account 1", names[0], True)
        l2 = Account("Account 2", names[1], False)

        l1.save(), l2.save() # hehe this is bad code

        response = self.client.get(reverse("accounts:hx-list"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["account_list"],
            [l1, l2],
            ordered = False
        )
