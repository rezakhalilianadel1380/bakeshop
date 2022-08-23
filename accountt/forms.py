from wsgiref.validate import validator
from django import forms
from .models import Address
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import CommonPasswordValidator,MinimumLengthValidator,NumericPasswordValidator
from django.contrib.auth.models import User







class User_Address(forms.ModelForm):
    class Meta:
        model = Address
        exclude=('user',)

    def __init__(self, *args, **kwargs):
        super(User_Address,self).__init__(*args, **kwargs)
        self.fields['state'].widget.attrs.update({'class': 'form-control'})
        self.fields['state'].widget.attrs['readonly'] = True
        self.fields['city'].widget.attrs['readonly'] = True
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control addtext'})
        self.fields['pelak'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahed'].widget.attrs.update({'class': 'form-control'})


class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name',"last_name",'email')

    def __init__(self, *args, **kwargs):
        super(User_Form,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
  



class Register(forms.Form):
    first_name = forms.CharField(validators=[
            RegexValidator(
                regex=r'^[^0-9]+$',
                message="نام شما باید شامل حروف وارد کنید",
            )],widget=forms.TextInput(
        attrs={
            'id':'firstname',
            "class":"form-control", 
            "placeholder":"نام",
            'maxlength':'50'
            }),

         )
    family = forms.CharField(validators=[
            RegexValidator(
                regex=r'^[^0-9]+$',
                message="نام و نام خانوادگی باید شامل حروف باشد",
            )],widget=forms.TextInput(
        attrs={
            "id":"lastname",
            "class":"form-control", 
            "placeholder":"نام خانوادگی",
            'maxlength':'50'
            }
    ),
    )
    password=forms.CharField(validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9]+$',
                message="باید شامل حروف انگلیسی و اعداد باشد ",
            )],widget=forms.TextInput(
        attrs={
            "id":"password" ,
            "class":"form-control",
            "placeholder":"رمز عبور",
            }
    ),
    )
    password_confirm=forms.CharField(widget=forms.TextInput(
        attrs={
            "id":"re_password" ,
            "class":"form-control",
            "placeholder":"تکرار رمز عبور",
            }
    ),
    )
   
    def clean_password_confirm(self):
        password=self.cleaned_data.get('password')
        confirm_password=self.cleaned_data.get('password_confirm')
        if password!=confirm_password:
            raise forms.ValidationError("رمز عبور با تکرار آن برابر نیست")
        return confirm_password


    def clean_password(self):
        password=self.cleaned_data.get('password')
        if password.isdigit():
            raise forms.ValidationError("رمز عبور نمیتواند تمام عدد باشد")
        if len(password)<8:
            raise forms.ValidationError("رمز عبور باید حداقل 8 کاراکتر باشد")
        return password

    
   
