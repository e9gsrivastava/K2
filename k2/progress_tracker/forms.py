from django import forms


class ProgressReportForm(forms.Form):
    marks = forms.IntegerField()
    comments = forms.CharField(widget=forms.Textarea)

    marks.widget.attrs.update({'class': 'form-control'})
    comments.widget.attrs.update({'class': 'form-control'})