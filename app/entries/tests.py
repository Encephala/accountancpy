from django.test import TestCase
from django.urls import reverse

from .models import Entry, EntryRow
from journals.models import Journal

# Create your tests here.
class EntriesViewsTest(TestCase):

    def setUp(self):
        self.journal1 = Journal(id = "Test journal")
        self.journal2 = Journal(id = "Second test journal")
        self.journal1.save()
        self.journal2.save()


    def test_entries_overview(self):
        response = self.client.get(reverse("entries:overview"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Overview of Entries")


    def test_entries_details(self):
        e = Entry(journal = self.journal1, notes = "A testing entry")
        e.save()

        response = self.client.get(reverse("entries:details", args = [e.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, e.journal.name)


    def test_entries_list_empty(self):
        response = self.client.get(reverse("entries:list"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["entry_list"], [])

    def test_entries_list_populated(self):
        notes = ["A testing entry", "Anutha one"]
        e1 = Entry(journal = self.journal1, notes = notes[0])
        e2 = Entry(journal = self.journal1, notes = notes[1])
        e1.save()
        e2.save()

        response = self.client.get(reverse("entries:list"))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["entry_list"],
            [e1, e2]
        )


class EntryRowViewsTest(TestCase):

    def setUp(self):
        self.journal1 = Journal(id = "Test journal")
        self.journal2 = Journal(id = "Second test journal")
        self.journal1.save()
        self.journal2.save()


    def test_entry_row_by_journal_other_journal(self):
        e = Entry(journal = self.journal2, notes = "A testing entry")
        e.save()

        response = self.client.get(reverse("entries:journal_rows", args = [self.journal1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["entry_list"],
            []
        )

    def test_entry_row_by_journal_same_journal(self):
        e = Entry(journal = self.journal1, notes = "A testing entry")
        e.save()

        response = self.client.get(reverse("entries:journal_rows", args = [self.journal1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["entry_list"],
            [e]
        )

    # TODO: Tests voor by-entry, by-ledger, by-account etc.
