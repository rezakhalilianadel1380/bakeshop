from django import forms
from bread.models import Bread
from accountt.models import User_detail,Setting
from django.contrib.auth.models import User
from order.models import Cart
from order.models import Discount
from bread.models import Bread_Attr


class Bread_Attr_Form(forms.ModelForm):
    class Meta:
        model = Bread_Attr
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super(Discount_Form,self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({'display': 'none'})
        


class Discount_Form(forms.ModelForm):
    class Meta:
        model = Discount
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super(Discount_Form,self).__init__(*args, **kwargs)
        self.fields['discount_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['dicount_percent'].widget.attrs.update({'class': 'form-control '})
        self.fields['max_price_dicount'].widget.attrs.update({'class': 'form-control '})
        self.fields['price_after_max_price'].widget.attrs.update({'class': 'form-control '})
        self.fields['active'].widget.attrs.update( {'class': 'flat-red'})


class Order_Form(forms.ModelForm):
    class Meta:
        model = Cart
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super(Order_Form,self).__init__(*args, **kwargs)
        self.fields['payment_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].widget.attrs.update({'class': 'form-control select2'})
        self.fields['delivery_mode'].widget.attrs.update({'class': 'form-control select2'})
        self.fields['status'].widget.attrs.update({'class': 'form-control select2'})
        self.fields['address'].widget.attrs.update({'class': 'form-control select2'})
        self.fields['is_paid'].widget.attrs.update( {'class': 'flat-red'})

class Setting_edite_Form(forms.ModelForm):
    class Meta:
        model = Setting
        fields="__all__"

    def __init__(self, *args, **kwargs):
        super(Setting_edite_Form,self).__init__(*args, **kwargs)
        self.fields['limit_day'].widget.attrs.update({'class': 'form-control'})
        self.fields['limit_buy'].widget.attrs.update({'class': 'form-control'})
        self.fields['is_on'].widget.attrs.update( {'class': 'flat-red'})
        





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
        self.fields['base_price'].widget.attrs.update({'class': 'form-control'})

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



