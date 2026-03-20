from django import forms

class UploadFileForm(forms.Form):
    dataset_name = forms.CharField(max_length=255, label="Dataset Name")
    file = forms.FileField(label="Upload CSV/Excel")
