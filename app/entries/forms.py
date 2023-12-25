from django import forms
from django.forms import BaseModelFormSet, modelformset_factory, BaseInlineFormSet, inlineformset_factory,\
    ValidationError

from .models import Entry, EntryRow

import logging
logger = logging.getLogger("django")


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Render widgets with Bootstrap styling
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

        # Smaller text for Notes
        self.fields["notes"].widget.attrs["class"] += " form-control-sm"


class EntryRowForm(forms.ModelForm):
    class Meta:
        model = EntryRow
        exclude = ["entry"]
        widgets = {
            "date": forms.DateInput(attrs = {"type":"date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Render widgets with Bootstrap styling
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class BaseEntryRowFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for entryrow_form in self.forms:
            # Force non-edited rows to still be validated
            entryrow_form.empty_permitted = False

            # Render the HTML required attribute
            entryrow_form.use_required_attribute = True

    def clean(self):
        super().clean()
        if any(self.errors):
            return

        sum_of_values = 0

        for entryrow_form in self.forms:
            if self.can_delete and self._should_delete_form(entryrow_form):
                continue

            sum_of_values += entryrow_form.cleaned_data["value"]

        if sum_of_values != 0:
            raise ValidationError("The rows in this entry don't sum to € 0,-. (€ %(sum)s)",
                                params = {"sum": sum_of_values}, code = "nonzero-sum")

class InlineEntryRowFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for entryrow_form in self.forms:
            # Force non-edited rows to still be validated
            entryrow_form.empty_permitted = False

            # Render the HTML required attribute
            entryrow_form.use_required_attribute = True

    def clean(self):
        super().clean()
        if any(self.errors):
            return

        sum_of_values = 0

        for entryrow_form in self.forms:
            if self.can_delete and self._should_delete_form(entryrow_form):
                continue

            sum_of_values += entryrow_form.cleaned_data["value"]

        if sum_of_values != 0:
            raise ValidationError("The rows in this entry don't sum to € 0,-. (€ %(sum)s)",
                                params = {"sum": sum_of_values}, code = "nonzero-sum")


EntryRowFormSet = modelformset_factory(EntryRow, form = EntryRowForm, formset = BaseEntryRowFormSet)
EntryRowUpdateFormSet = inlineformset_factory(Entry, EntryRow, form = EntryRowForm, formset = InlineEntryRowFormSet,
                                              extra = 1)
