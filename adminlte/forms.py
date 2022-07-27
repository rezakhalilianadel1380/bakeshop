from django import forms
from bread.models import Bread
from accountt.models import User_detail
from django.contrib.auth.models import User






class login_form(forms.Form):
    username = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
            "class":"form-control", 
            "placeholder":" نام کاربری",
            'maxlength':'50',
            }),

        )
    password = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
            "class":"form-control", 
            "placeholder":"گذرواژه",
            'maxlength':'50',
            }
    ),
    )





class User_Detail_Form(forms.ModelForm):
    class Meta:
        model = User_detail
        exclude = ('user',)

       



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

class User_Form(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('date_joined','last_login')

    def __init__(self, *args, **kwargs):
        super(User_Form,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['groups'].widget.attrs.update(
            {'class': 'form-control  select2'})
        self.fields['user_permissions'].widget.attrs.update(
            {'class': 'form-control  select2'})
        self.fields['is_active'].widget.attrs.update(
            {'class': 'flat-red'})
        self.fields['is_staff'].widget.attrs.update(
            {'class': 'flat-red'})
        self.fields['is_superuser'].widget.attrs.update(
            {'class': 'flat-red'})



