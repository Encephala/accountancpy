from django.test import TestCase
from django.urls import reverse

from .models import *

# Create your tests here.
class JournalsViewsTest(TestCase):

    # Create journal and see if it's in the rendered list
    def test_journal_overview(self):
        response = self.client.get(reverse("journals:overview"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Overview of Journals")


    def test_journal_details(self):
        l1 = Journal("test", "a testing Journal", "INC")
        l1.save()

        response = self.client.get(reverse("journals:details", args = [l1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, l1.name)


    def test_journal_list_empty(self):
        response = self.client.get(reverse("journals:hx-list"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["journal_list"],
            []
        )

    def test_journal_list_populated(self):
        names = ["A testing Journal", "A second one"]
        l1 = Journal("Journal 1", names[0], "INC")
        l2 = Journal("Journal 2", names[1], "EXP")

        l1.save(), l2.save() # hehe this is bad code

        response = self.client.get(reverse("journals:hx-list"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["journal_list"],
            [l1, l2],
            ordered = False
        )
