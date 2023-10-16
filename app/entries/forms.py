import datetime

from django import forms

from .models import Entry, EntryRow


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
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(format = ("%Y/%m/%d"), attrs = {"class":"form-control", "type":"date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Render widgets with Bootstrap styling
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
