from django.test import TestCase
from django.urls import reverse

from .models import Entry, EntryRow
from journals.models import Journal
from accounts.models import Account
from ledgers.models import Ledger

# Create your tests here.
class EntriesViewsTest(TestCase):

    def setUp(self):
        self.journal1 = Journal(id = "journ1")
        self.journal2 = Journal(id = "journ2")
        self.journal1.save()
        self.journal2.save()

        self.account1 = Account(id = "acc1", name = "Test account 1", is_creditor = True)
        self.account2 = Account(id = "acc2", name = "Test account 2", is_creditor = False)
        self.account1.save()
        self.account2.save()

        self.ledger1 = Ledger(id = "test1", name = "Test ledger 1", type = "INC")
        self.ledger2 = Ledger(id = "test2", name = "Test ledger 2", type = "EXP")
        self.ledger1.save()
        self.ledger2.save()


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


    def test_entries_create(self):
        data = {
            'journal': ['journ1'], 'notes': [''], 'form-TOTAL_FORMS': ['3'],
             'form-INITIAL_FORMS': ['0'], 'form-MIN_NUM_FORMS': ['0'], 'form-MAX_NUM_FORMS': ['1000'],
             'form-0-id': [''], 'form-0-date': ['2023-12-27'], 'initial-form-0-date': ['2023-12-27', '', ''],
             'form-0-ledger': ['test1'], 'form-0-account': ['acc1'], 'form-0-value': ['69'], 'form-1-id': [''],
             'form-1-DELETE': [''], 'form-1-date': ['2023-12-27'], 'form-1-ledger': ['test2'],
             'form-1-account': ['acc2'], 'form-1-value': ['-60'], 'form-2-id': [''], 'form-2-DELETE': [''],
             'form-2-date': ['2023-12-27'], 'form-2-ledger': ['test2'], 'form-2-account': ['acc1'],
             'form-2-value': ['-9']
        }

        response = self.client.post(reverse("entries:create"), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(EntryRow.objects.count(), 3)

    def test_entries_create_fails(self):
        # Data doesn't sum to 0
        data = {
            'journal': ['journ1'], 'notes': [''], 'form-TOTAL_FORMS': ['2'],
             'form-INITIAL_FORMS': ['0'], 'form-MIN_NUM_FORMS': ['0'], 'form-MAX_NUM_FORMS': ['1000'],
             'form-0-id': [''], 'form-0-date': ['2023-12-27'], 'initial-form-0-date': ['2023-12-27', '', ''],
             'form-0-ledger': ['test1'], 'form-0-account': ['acc1'], 'form-0-value': ['2'], 'form-1-id': [''],
             'form-1-DELETE': [''], 'form-1-date': ['2023-12-27'], 'form-1-ledger': ['test2'],
             'form-1-account': ['acc2'], 'form-1-value': ['-3']
        }

        response = self.client.post(reverse("entries:create"), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Entry.objects.count(), 0)
        self.assertEqual(EntryRow.objects.count(), 0)
        self.assertContains(response, "The rows in this entry")

        # Wrong number of forms
        data = {
            'journal': ['journ1'], 'notes': [''], 'form-TOTAL_FORMS': ['1'],
             'form-INITIAL_FORMS': ['0'], 'form-MIN_NUM_FORMS': ['0'], 'form-MAX_NUM_FORMS': ['1000'],
             'form-0-id': [''], 'form-0-date': ['2023-12-27'], 'initial-form-0-date': ['2023-12-27', '', ''],
             'form-0-ledger': ['test1'], 'form-0-account': ['acc1'], 'form-0-value': ['2'], 'form-1-id': [''],
             'form-1-DELETE': [''], 'form-1-date': ['2023-12-27'], 'form-1-ledger': ['test2'],
             'form-1-account': ['acc2'], 'form-1-value': ['-2']
        }

        response = self.client.post(reverse("entries:create"), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Entry.objects.count(), 0)
        self.assertEqual(EntryRow.objects.count(), 0)

        # Missing data
        data = {
            'journal': ['journ1'], 'notes': [''], 'form-TOTAL_FORMS': ['2'],
             'form-INITIAL_FORMS': ['0'], 'form-MIN_NUM_FORMS': ['0'], 'form-MAX_NUM_FORMS': ['1000'],
             'form-0-id': [''], 'form-0-date': ['2023-12-27'], 'initial-form-0-date': ['2023-12-27', '', ''],
             'form-0-ledger': ['test1'], 'form-0-account': ['acc1'], 'form-0-value': ['0']
        }

        response = self.client.post(reverse("entries:create"), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Entry.objects.count(), 0)
        self.assertEqual(EntryRow.objects.count(), 0)


    def test_entries_update(self):
        # Entry to be updated
        pre_data = {
            'journal': ['journ1'], 'notes': [''], 'form-TOTAL_FORMS': ['3'],
             'form-INITIAL_FORMS': ['0'], 'form-MIN_NUM_FORMS': ['0'], 'form-MAX_NUM_FORMS': ['1000'],
             'form-0-id': [''], 'form-0-date': ['2023-12-27'], 'initial-form-0-date': ['2023-12-27', '', ''],
             'form-0-ledger': ['test1'], 'form-0-account': ['acc1'], 'form-0-value': ['69'], 'form-1-id': [''],
             'form-1-DELETE': [''], 'form-1-date': ['2023-12-27'], 'form-1-ledger': ['test2'],
             'form-1-account': ['acc2'], 'form-1-value': ['-60'], 'form-2-id': [''], 'form-2-DELETE': [''],
             'form-2-date': ['2023-12-27'], 'form-2-ledger': ['test2'], 'form-2-account': ['acc1'],
             'form-2-value': ['-9']
        }

        self.client.post(reverse("entries:create"), pre_data)

        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(EntryRow.objects.count(), 3)

        # Update values
        data = {
            'journal': ['journ2'], 'notes': [''], 'entryrow_set-TOTAL_FORMS': ['3'],
            'entryrow_set-INITIAL_FORMS': ['3'], 'entryrow_set-MIN_NUM_FORMS': ['0'],
            'entryrow_set-MAX_NUM_FORMS': ['1000'], 'entryrow_set-0-id': ['1'],
            'entryrow_set-0-date': ['2023-12-27'], 'initial-entryrow_set-0-date': ['2023-12-27'],
            'entryrow_set-0-ledger': ['test1'], 'entryrow_set-0-account': [''], 'entryrow_set-0-value': ['1.00'],
            'entryrow_set-1-id': ['2'], 'entryrow_set-1-date': ['2023-12-27'],
            'initial-entryrow_set-1-date': ['2023-12-27'], 'entryrow_set-1-ledger': ['test2'],
            'entryrow_set-1-account': [''], 'entryrow_set-1-value': ['2.00'], 'entryrow_set-2-id': ['3'],
            'entryrow_set-2-date': ['2023-12-27'], 'initial-entryrow_set-2-date': ['2023-12-27'],
            'entryrow_set-2-ledger': ['test1'], 'entryrow_set-2-account': [''], 'entryrow_set-2-value': ['-3.00']
        }

        response = self.client.post(reverse("entries:update", kwargs = {"pk": 1}), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(EntryRow.objects.count(), 3)
        self.assertEqual(EntryRow.objects.get(pk = 1).value, 1.00)

        # Ignore deleted forms
        data = {
            'journal': ['journ2'], 'notes': [''], 'entryrow_set-TOTAL_FORMS': ['3'],
            'entryrow_set-INITIAL_FORMS': ['3'], 'entryrow_set-MIN_NUM_FORMS': ['0'],
            'entryrow_set-MAX_NUM_FORMS': ['1000'], 'entryrow_set-0-id': ['1'],
            'entryrow_set-0-date': ['2023-12-27'], 'initial-entryrow_set-0-date': ['2023-12-27'],
            'entryrow_set-0-ledger': ['test1'], 'entryrow_set-0-account': [''], 'entryrow_set-0-value': ['69.00'],
            'entryrow_set-1-id': ['2'], 'entryrow_set-1-DELETE': ['on'], 'entryrow_set-1-date': ['2023-12-27'],
            'initial-entryrow_set-1-date': ['2023-12-27'], 'entryrow_set-1-ledger': ['test2'],
            'entryrow_set-1-account': [''], 'entryrow_set-1-value': ['-60.00'], 'entryrow_set-2-id': ['3'],
            'entryrow_set-2-date': ['2023-12-27'], 'initial-entryrow_set-2-date': ['2023-12-27'],
            'entryrow_set-2-ledger': ['test1'], 'entryrow_set-2-account': [''], 'entryrow_set-2-value': ['-69.00']
        }

        response = self.client.post(reverse("entries:update", kwargs = {"pk": 1}), data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(EntryRow.objects.count(), 2)
        self.assertEqual(EntryRow.objects.get(pk = 1).value, 69.00)

    def test_entries_update_fails(self):
        # Entry to be updated
        pre_data = {
            'journal': ['journ1'], 'notes': [''], 'form-TOTAL_FORMS': ['3'],
             'form-INITIAL_FORMS': ['0'], 'form-MIN_NUM_FORMS': ['0'], 'form-MAX_NUM_FORMS': ['1000'],
             'form-0-id': [''], 'form-0-date': ['2023-12-27'], 'initial-form-0-date': ['2023-12-27', '', ''],
             'form-0-ledger': ['test1'], 'form-0-account': ['acc1'], 'form-0-value': ['69'], 'form-1-id': [''],
             'form-1-DELETE': [''], 'form-1-date': ['2023-12-27'], 'form-1-ledger': ['test2'],
             'form-1-account': ['acc2'], 'form-1-value': ['-60'], 'form-2-id': [''], 'form-2-DELETE': [''],
             'form-2-date': ['2023-12-27'], 'form-2-ledger': ['test2'], 'form-2-account': ['acc1'],
             'form-2-value': ['-9']
        }

        self.client.post(reverse("entries:create"), pre_data)

        self.assertEqual(EntryRow.objects.count(), 3)

        # Data doesn't sum to 0
        data = {
            'journal': ['journ2'], 'notes': [''], 'entryrow_set-TOTAL_FORMS': ['3'],
            'entryrow_set-INITIAL_FORMS': ['3'], 'entryrow_set-MIN_NUM_FORMS': ['0'],
            'entryrow_set-MAX_NUM_FORMS': ['1000'], 'entryrow_set-0-id': ['1'],
            'entryrow_set-0-date': ['2023-12-27'], 'initial-entryrow_set-0-date': ['2023-12-27'],
            'entryrow_set-0-ledger': ['test1'], 'entryrow_set-0-account': [''], 'entryrow_set-0-value': ['12345'],
            'entryrow_set-1-id': ['2'], 'entryrow_set-1-date': ['2023-12-27'],
            'initial-entryrow_set-1-date': ['2023-12-27'], 'entryrow_set-1-ledger': ['test2'],
            'entryrow_set-1-account': [''], 'entryrow_set-1-value': ['2.00'], 'entryrow_set-2-id': ['3'],
            'entryrow_set-2-date': ['2023-12-27'], 'initial-entryrow_set-2-date': ['2023-12-27'],
            'entryrow_set-2-ledger': ['test1'], 'entryrow_set-2-account': [''], 'entryrow_set-2-value': ['-3.00']
        }

        response = self.client.post(reverse("entries:update", kwargs = {"pk": 1}), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(EntryRow.objects.get(pk = 1).value, 69.00)
        self.assertContains(response, "The rows in this entry")


    def test_entries_delete(self):
        # Entry to be updated
        pre_data = {
            'journal': ['journ1'], 'notes': [''], 'form-TOTAL_FORMS': ['3'],
             'form-INITIAL_FORMS': ['0'], 'form-MIN_NUM_FORMS': ['0'], 'form-MAX_NUM_FORMS': ['1000'],
             'form-0-id': [''], 'form-0-date': ['2023-12-27'], 'initial-form-0-date': ['2023-12-27', '', ''],
             'form-0-ledger': ['test1'], 'form-0-account': ['acc1'], 'form-0-value': ['69'], 'form-1-id': [''],
             'form-1-DELETE': [''], 'form-1-date': ['2023-12-27'], 'form-1-ledger': ['test2'],
             'form-1-account': ['acc2'], 'form-1-value': ['-60'], 'form-2-id': [''], 'form-2-DELETE': [''],
             'form-2-date': ['2023-12-27'], 'form-2-ledger': ['test2'], 'form-2-account': ['acc1'],
             'form-2-value': ['-9']
        }

        self.client.post(reverse("entries:create"), pre_data)

        self.assertEqual(Entry.objects.count(), 1)

        response = self.client.post(reverse("entries:delete", kwargs = {"pk": 1}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.count(), 0)


class EntryFilteredViewsTest(TestCase):
    def setUp(self):
        self.journal1 = Journal(id = "Test journal")
        self.journal2 = Journal(id = "Second test journal")
        self.journal1.save()
        self.journal2.save()

        self.account1 = Account(id = "acc1", name = "Test account 1", is_creditor = True)
        self.account2 = Account(id = "acc2", name = "Test account 2", is_creditor = False)
        self.account1.save()
        self.account2.save()

        self.ledger1 = Ledger(id = "test1", name = "Test ledger 1", type = "INC")
        self.ledger2 = Ledger(id = "test2", name = "Test ledger 2", type = "EXP")
        self.ledger1.save()
        self.ledger2.save()


    def test_entry_by_journal(self):
        e1 = Entry(journal = self.journal1, notes = "A testing entry")
        e2 = Entry(journal = self.journal2, notes = "A testing entry")
        e1.save()
        e2.save()

        response = self.client.get(reverse("entries:journal_rows", args = [self.journal1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["entry_list"],
            [e1]
        )

    def test_entry_row_by_ledger(self):
        e = Entry(journal = self.journal1, notes = "A testing entry")
        e.save()

        er1 = EntryRow(entry = e, ledger = self.ledger1, account = self.account1, value = 69)
        er2 = EntryRow(entry = e, ledger = self.ledger2, account = self.account2, value = -69)
        er1.save()
        er2.save()

        response = self.client.get(reverse("entries:ledger_rows", args = [self.ledger1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["entry_row_list"],
            [er1]
        )

    def test_entry_row_by_entry(self):
        e1 = Entry(journal = self.journal1, notes = "A testing entry")
        e2 = Entry(journal = self.journal1, notes = "A second testing entry")
        e1.save()
        e2.save()

        er1 = EntryRow(entry = e1, ledger = self.ledger1, account = self.account1, value = 69)
        er2 = EntryRow(entry = e2, ledger = self.ledger1, account = self.account1, value = -69)
        er1.save()
        er2.save()

        response = self.client.get(reverse("entries:entry_rows", args = [e1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["entry_row_list"],
            [er1]
        )

    def test_entry_row_by_account(self):
        e1 = Entry(journal = self.journal1, notes = "A testing entry")
        e2 = Entry(journal = self.journal1, notes = "A second testing entry")
        e1.save()
        e2.save()

        er1 = EntryRow(entry = e1, ledger = self.ledger1, account = self.account1, value = 69)
        er2 = EntryRow(entry = e1, ledger = self.ledger2, account = self.account2, value = -69)
        er1.save()
        er2.save()

        response = self.client.get(reverse("entries:account_rows", args = [self.account1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["entry_row_list"],
            [er1]
        )
