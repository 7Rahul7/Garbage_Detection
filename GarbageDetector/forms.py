from django import forms
from .models import Upload

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none'
            })
        }
        labels = {
            'file': 'Upload Image'
        }