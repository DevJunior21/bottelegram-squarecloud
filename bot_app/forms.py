from django import forms
from .models import MensagemPromocional

class MensagemPromocionalForm(forms.ModelForm):
    class Meta:
        model = MensagemPromocional
        fields = '__all__'