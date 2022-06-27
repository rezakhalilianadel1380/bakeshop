from django import forms
from django.core.validators import RegexValidator


radio_choices = (('1','حضوری'), ('2', 'پیک'))

class Cart_Form(forms.Form):
    bread_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class":"form-control",
        "min":"1",
        "max":"15",
        "value":"1",
        "oninvalid":"setCustomValidity('تعداد نان باید در بازه یک تا 15 عدد باشد')" ,
        "oninput":"setCustomValidity('')",
    }))

    def clean_quantity(self):
        quantity=self.cleaned_data.get('quantity')
        if quantity>15 or quantity<1:
            raise forms.ValidationError('تعداد نان باید در بازه یک تا 15 عدد باشد ')
        return quantity


