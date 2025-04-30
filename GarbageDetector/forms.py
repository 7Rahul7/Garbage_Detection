from django import forms
from .models import Upload

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['file']



