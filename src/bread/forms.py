from django import forms
from .models import Bread


class Bread_Form(forms.Form):
    bread_attr=forms.ChoiceField(required=False,
        widget=forms.Select(
        attrs={
            "class":"form-control mt-2", 
            "placeholder":" نام کاربری",
            
            }),

                                 )
    


       


