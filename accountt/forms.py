from wsgiref.validate import validator
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import CommonPasswordValidator,MinimumLengthValidator,NumericPasswordValidator


class Phone_login_form(forms.Form):
    phone = forms.CharField(validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message="شماره تلفن را به شکل درست وارد کنید",
            )
        ],widget=forms.TextInput(
        attrs={
            "id":"phone" ,
            "class":"form-control", 
            "placeholder":"شماره تلفن همراه",
            }),

         )
    
    # def clean_phone(self):
    #     phone=self.cleaned_data.get('phone')
       
    #     if  len(phone) !=11 or phone[0]!='0':
    #         raise forms.ValidationError("شماره تلفن همراه صحیح نیست")
    #     return phone

     
class password_login_form(forms.Form):
    password = forms.CharField(widget=forms.TextInput(
        attrs={
            "id":"password" ,
            "class":"form-control", 
            "placeholder":"رمز عبور",
            }),

         )


class code_login_form(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={
            "id":"code" ,
            "class":"form-control", 
            "placeholder":"کد تایید",
            
            }),

         )

class Code_register_form(forms.Form):
    codes = forms.CharField(widget=forms.TextInput(
        attrs={
            "id":"code" ,
            "class":"form-control", 
            "placeholder":"کد تایید",
            
            }),

         )

class Phone_register_form(forms.Form):
    phone = forms.CharField(validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message="شماره تلفن را به شکل درست وارد کنید",
            )
        ],widget=forms.TextInput(
        attrs={
            "id":"phone" ,
            "class":"form-control", 
            "placeholder":"شماره تلفن همراه",
            }),

         )


class Register(forms.Form):
    name = forms.CharField(validators=[
            RegexValidator(
                regex=r'^[^0-9]+$',
                message="نام شما باید شامل حروف وارد کنید",
            )],widget=forms.TextInput(
        attrs={
            "id":"name" ,
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
            "id":"family" ,
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
            "id":"password_confirm" ,
            "class":"form-control",
            "placeholder":"تکرار رمز عبور",
            }
    ),
    )
    address=forms.CharField(widget=forms.Textarea(
        attrs={
            "id":"address" ,
            "class":"form-control",
            "placeholder":"آدرس",
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

    def clean_name(self):
        name:str=self.cleaned_data.get('name')
        name=name.strip()
        return name
    
   
