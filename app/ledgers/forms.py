from django import forms

from .models import Ledger

class LedgerForm(forms.ModelForm):
    class Meta:
        model = Ledger
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(LedgerForm, self).__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

        self.fields["notes"].widget.attrs["class"] += " form-control-sm"
