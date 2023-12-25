from django import forms
from django.forms import BaseModelFormSet, modelformset_factory, ValidationError

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
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs = {"type":"date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Force non-edited rows to still be validated
        self.empty_permitted = False

        # Render widgets with Bootstrap styling
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"


class BaseEntryRowFormSet(BaseModelFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        sum_of_values = 0

        for entryrow in self.forms:
            if self.can_delete and self._should_delete_form(entryrow):
                continue

            sum_of_values += entryrow.cleaned_data["value"]

        if sum_of_values != 0:
            raise ValidationError("The rows in this entry don't sum to € 0,-. (€ %(sum)s)",
                                params = {"sum": sum_of_values}, code = "nonzero-sum")


EntryRowFormSet = modelformset_factory(EntryRow, fields = "__all__", form = EntryRowForm,
                                       formset = BaseEntryRowFormSet)
