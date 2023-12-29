from django.test import TestCase
from django.urls import reverse

from .models import Journal

# Create your tests here.
class JournalsViewsTest(TestCase):

    # Create journal and see if it's in the rendered list
    def test_journal_details(self):
        j1 = Journal("test", "a testing Journal", "INC")
        j1.full_clean()
        j1.save()

        response = self.client.get(reverse("journals:details", args = [j1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, j1.name)


    def test_journal_list_populated(self):
        names = ["A testing Journal", "A second one"]
        j1 = Journal("Journal 1", names[0], "INC")
        j2 = Journal("Journal 2", names[1], "EXP")

        j1.full_clean(), j2.full_clean() # hehe this is bad code
        j1.save(), j2.save()

        response = self.client.get(reverse("journals:hx-list"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["journal_list"],
            [j1, j2],
            ordered = False
        )
