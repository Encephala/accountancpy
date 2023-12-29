from django.test import TestCase
from django.urls import reverse

from .models import Account

# Create your tests here.
class AccountsViewsTest(TestCase):

    # Create account and see if it's in the rendered list
    def test_account_details(self):
        a1 = Account("test", "a testing Account", True)
        a1.full_clean()
        a1.save()

        response = self.client.get(reverse("accounts:details", args = [a1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, a1.name)


    def test_account_list_populated(self):
        names = ["A testing Account", "A second one"]
        a1 = Account("Account 1", names[0], True)
        a2 = Account("Account 2", names[1], False)

        a1.full_clean(), a2.full_clean() # hehe this is bad code
        a1.save(), a2.save()

        response = self.client.get(reverse("accounts:hx-list"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["account_list"],
            [a1, a2],
            ordered = False
        )
