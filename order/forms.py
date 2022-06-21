from django import forms
from django.core.validators import RegexValidator


radio_choices = (('1','حضوری'), ('2', 'پیک'))

class Cart_Form(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class":"form-control",
        "min":"1",
        "max":"15",
        "value":"1",
    }))

