
from django import forms
from .models import ImportedData


class DataImportForm(forms.Form):
    file = forms.FileField(required=False)


class ImportedDataForm(forms.ModelForm):
    class Meta:
        model = ImportedData
        fields = ['column_name', 'column_type', 'column_required']
