import logging

from django import forms
from django.forms import (
    BaseInlineFormSet,
    BaseModelFormSet,
    ValidationError,
    inlineformset_factory,
    modelformset_factory,
)

from .models import Entry, EntryRow

logger = logging.getLogger("django")


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["journal", "notes"]

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
        # Excludes "entry" field
        fields = ["date", "ledger", "account", "document", "value"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
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
            entryrow_form.empty_permitted = True

            # Render the HTML required attribute
            entryrow_form.use_required_attribute = True

    def clean(self):
        super().clean()
        if any(self.errors):
            return

        sum_of_values = 0

        for entryrow_form in self.forms:
            if entryrow_form.empty_permitted and not entryrow_form.has_changed():
                continue

            if self.can_delete and self._should_delete_form(entryrow_form):
                continue

            sum_of_values += entryrow_form.cleaned_data["value"]

        if sum_of_values != 0:
            error_msg = "The rows in this entry don't sum to € 0,-. (sum = € %(sum)s)"
            raise ValidationError(
                error_msg,
                params={"sum": sum_of_values},
                code="nonzero-sum",
            )


class InlineEntryRowFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for entryrow_form in self.forms:
            # Force non-edited rows to still be validated
            # so that the clean method below works
            entryrow_form.empty_permitted = False

            # Render the HTML required attribute
            entryrow_form.use_required_attribute = True

    def clean(self):
        super().clean()
        if any(self.errors):
            return

        sum_of_values = 0

        for entryrow_form in self.forms:
            if entryrow_form.empty_permitted and not entryrow_form.has_changed():
                continue

            if self.can_delete and self._should_delete_form(entryrow_form):
                continue

            sum_of_values += entryrow_form.cleaned_data["value"]

        if sum_of_values != 0:
            error_msg = "The rows in this entry don't sum to € 0,-. (sum = € %(sum)s)"
            raise ValidationError(
                error_msg,
                params={"sum": sum_of_values},
                code="nonzero-sum",
            )


EntryRowFormSet = modelformset_factory(EntryRow, form=EntryRowForm, formset=BaseEntryRowFormSet)
EntryRowUpdateFormSet = inlineformset_factory(
    Entry,
    EntryRow,
    form=EntryRowForm,
    formset=InlineEntryRowFormSet,
    can_delete=True,
    extra=0,
)
