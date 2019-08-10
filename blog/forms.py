from django import forms

from .models import CV
from .models import Post


class CVForm(forms.ModelForm):

    class Meta:
        model = CV
        fields = ['pdf']












