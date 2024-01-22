from django import forms


class ProgressReportForm(forms.Form):
    progress_report_id = forms.IntegerField(widget=forms.HiddenInput())
    marks = forms.IntegerField()
    comments = forms.CharField(widget=forms.Textarea)

    progress_report_id.widget.attrs.update({'class': 'form-control'})
    marks.widget.attrs.update({'class': 'form-control'})
    comments.widget.attrs.update({'class': 'form-control'})