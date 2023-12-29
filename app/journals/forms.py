from django import forms

from .models import Journal

class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Render widgets with Bootstrap styling
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

        # Smaller text for Notes
        self.fields["notes"].widget.attrs["class"] += " form-control-sm"

    def clean_id(self):
        id = self.cleaned_data["id"]

        if id in ["create", "hx-list"]:
            raise forms.ValidationError("That ID is a reserved name", code = "pk-reserved-name")

        return id
