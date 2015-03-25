from django import forms

from uw_reports.models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'
