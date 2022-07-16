from django import forms
from bread.models import Bread

class Bread_Form(forms.ModelForm):
    class Meta:
        model = Bread
        exclude = ('users',)

    def __init__(self, *args, **kwargs):
        super(Bread_Form,self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})

