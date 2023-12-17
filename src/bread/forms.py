from django import forms
from .models import Bread


class Bread_Form(forms.Form):
    bread_attr=forms.ChoiceField(choices=[],required=False)
       


