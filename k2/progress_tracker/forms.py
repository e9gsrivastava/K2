from django import forms
from .models import ProgressReport


class ProgressReportForm(forms.ModelForm):
    class Meta:
        model = ProgressReport
        fields = ["marks", "comments"]

    def __init__(self, *args, **kwargs):
        super(ProgressReportForm, self).__init__(*args, **kwargs)
        self.fields["marks"].widget.attrs.update({"class": "form-control"})
        self.fields["comments"].widget.attrs.update({"class": "form-control"})
