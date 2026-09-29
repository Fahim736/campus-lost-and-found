from django import forms
from .models import Report


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report

        fields = [
            'item_name',
            'type',
            'category',
            'description',
            'location',
            'date',
            'contact',
            'image',
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'description': forms.Textarea(
                attrs={'rows': 4}
            ),
        }