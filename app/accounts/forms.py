from django import forms

from .models import Account


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["id", "name", "is_creditor", "notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Render widgets with Bootstrap styling
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

        # Smaller text for Notes
        self.fields["notes"].widget.attrs["class"] += " form-control-sm"

    def clean_id(self):
        pk = self.cleaned_data["id"]

        if pk in ["create", "hx-list"]:
            error_msg = "That ID is a reserved name"
            raise forms.ValidationError(error_msg, code="pk-reserved-name")

        return pk
