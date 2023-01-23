from wsgiref.validate import validator
from django import forms
from .models import Address,Code,Sign_up
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import CommonPasswordValidator,MinimumLengthValidator,NumericPasswordValidator
from django.contrib.auth.models import User



class Chang_Phone(forms.Form):
    previous_phone_confirm_code = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
            "class":"form-control", 
            "placeholder":"کدتایید",
            'maxlength':'50'
            }),
    )
    new_phone_number = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
            "class":"form-control", 
            "placeholder":"شماره همراه",
            'maxlength':'50'
            }),
    )
    new_phone_confirm_code = forms.CharField(required=True,widget=forms.TextInput(
        attrs={
            "class":"form-control", 
            "placeholder":"کدتایید",
            'maxlength':'50'
            }),
    )

   



class Change_Password(forms.Form):
    previous_pass=forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"form-control", 
            "placeholder":"پسورد قبلی",
            'maxlength':'50'
            }),

         )

    password = forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"form-control", 
            "placeholder":" پسورد جدید",
            'maxlength':'50'
            }),

         )
    confirm_pass = forms.CharField(widget=forms.TextInput(
        attrs={
            "class":"form-control", 
            "placeholder":"تایید گذرواژه",
            'maxlength':'50'
            }),

         )

    def clean_confirm_pass(self):
        password=self.cleaned_data.get('password')
        confirm_password=self.cleaned_data.get('confirm_pass')
        if password!=confirm_password:
            raise forms.ValidationError("رمز عبور با تکرار آن برابر نیست")
        return confirm_password



class User_Address(forms.ModelForm):
    class Meta:
        model = Address
        exclude=('user',)
        widgets = {
            'lat': forms.HiddenInput(),
            'lon': forms.HiddenInput(),
            'pelak': forms.TextInput(),
            'vahed': forms.TextInput(),
        }


    def __init__(self, *args, **kwargs):
        super(User_Address,self).__init__(*args, **kwargs)
        self.fields['lat'].error_messages = {'required': 'از نقشه بالا موقعیت جغرافیایی خود را وارد کنید '}
        self.fields['lon'].error_messages = {'required':  'از نقشه بالا موقعیت جغرافیایی خود را وارد کنید '}
        self.fields['state'].widget.attrs.update({'class': 'form-control'})
        self.fields['state'].widget.attrs['disabled'] = True
        self.fields['city'].widget.attrs['disabled'] = True
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'class': 'form-control addtext'})
        self.fields['pelak'].widget.attrs.update({'class': 'form-control'})
        self.fields['vahed'].widget.attrs.update({'class': 'form-control'})
       


class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name',"last_name",'email')

    def __init__(self, *args, **kwargs):
        super(User_Form,self).__init__(*args, **kwargs)
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

    
   
