from django import forms
from .models import Bread


class Bread_Form(forms.ModelForm):
    class Meta:
        model = Bread
        fields=('title',)

    def __init__(self, *args, **kwargs):
        super(Bread_Form,self).__init__(*args, **kwargs)
       


