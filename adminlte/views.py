from django.shortcuts import redirect, render
from bread.models import Bread
from order.models import Cart
from order.models import Discount
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from accountt.models import Setting, User_detail
from rest_framework import status
from django.contrib import messages
from .forms import Bread_Form,User_Detail_Form,Order_Form,User_Form,login_form,Setting_edite_Form,Discount_Form
from django.contrib.auth.password_validation import validate_password
import re
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.exceptions import ValidationError,FieldError
import datetime
from django.db.models import Q
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout,authenticate,login
from accountt.models import Setting
from .permissions import Is_View_Cart,Read_Only,Bread_permission,Change_Cart_Permisson,Setting_Permission,User_Delete_Permission
from rest_framework import permissions
from sms_configure.sms import send_message
from django.http import Http404,HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import jdatetime



# from django.contrib.auth import mixins 
# from .serializers import Bread_Serializer
# from rest_framework.exceptions import PermissionDenied
# from rest_framework import generics
# from django.http import Http404
import os
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT,TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle 
from bidi.algorithm import get_display
from rtl import reshaper
import textwrap
import datetime
from  reportlab.lib import  pagesizes
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph,Table, TableStyle,Spacer,HRFlowable
from reportlab.lib import colors
from shop.settings import BASE_DIR
import io
from django.http import FileResponse
from jalali_date import datetime2jalali, date2jalali
import xlwt
# Create your views here.





def edite_discount(request,id):
    object_discount=Discount.objects.filter(id=id).first()
    form=Discount_Form(request.POST or None,instance=object_discount)
    if form.is_valid():
        form.save()
        messages.success(request,'باموفقیت ویرایش شد ')
        return redirect('/adminlte/discount')
    context={
        'form':form
    }
    return render(request,'edite_discount.html',context)


def add_discount(request):
    form=Discount_Form(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,'باموفقیت ایجاد شد ')
        return redirect('/adminlte/discount')
    context={
        'form':form
    }
    return render(request,'add_discount.html',context)



def show_discount(request):
    discounts=Discount.objects.all()
    paginator = Paginator(discounts,20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'page_obj':page_obj,
        
    }
    return render(request,'discount.html',context)


@user_passes_test(lambda u: u.has_perm('order.change_cart'),login_url='/adminlte/login')
def show_order_detail(request,id):
    cart=Cart.objects.filter(id=id)
    if not cart.exists():
        raise Http404
    form=Order_Form(request.POST  or None,instance=cart.first())
    if form.is_valid():
        form.save()
        messages.success(request,'ویرایش با موفقیت اعمال شد ')
        return redirect('/adminlte/show_orders') 
    context={
        'form':form
    }
    return render(request,"order_edite.html",context)


@user_passes_test(lambda u: u.has_perm('accountt.change_setting'),login_url='/adminlte/login')
def setting_edite(request,id):
    setting=Setting.objects.filter(id=1).first()
    form=Setting_edite_Form(request.POST or None,instance=setting)
    if form.is_valid():
        form.save()
        return redirect('/adminlte/setting')

    context={
        'form':form,
    }
    return render(request,'setting_edite.html',context)




@user_passes_test(lambda u: u.has_perm('accountt.view_setting'),login_url='/adminlte/login')
def setting_site(request):
    setting=Setting.objects.filter(id=1).first()
    context={
        'setting':setting
    }
    return render(request,'setting.html',context)




def admin_logout(request):
    logout(request)
    return redirect('/adminlte/login')


def admin_login(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('/adminlte')
    form=login_form(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_staff:
                login(request,user)
                next_page=request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('/adminlte')
            form.add_error('username','اجازه دسترسی داده نشد')
        else:
            form.add_error('username','کاربر یافت نشد ')
    context={
        'form':form
    }
    return render(request,'login_admin.html',context)




@user_passes_test(lambda u: u.is_superuser,login_url='/adminlte/login')
def show_orders(request):
    carts=Cart.objects.all().order_by('-payment_date')
    if request.GET.get('filter_time') and request.GET.get('filter_time')=='1' :
       carts=carts.filter(payment_date__date=timezone.now().date())
    elif  request.GET.get('filter_time') and request.GET.get('filter_time')=='2' :
       carts=carts.filter(payment_date__month=timezone.now().month,payment_date__year=timezone.now().year)
    elif request.GET.get('filter_time') and request.GET.get('filter_time')=='3' :
       carts=carts.filter(payment_date__year=timezone.now().year)
    if request.GET.get('qs'):
        q=request.GET.get('qs')
        lookup=(
           Q(user__username=q)|
           Q(user__first_name__contains=q)|
           Q(user__last_name__contains=q)
        )
        carts=Cart.objects.filter(lookup).distinct()
    paginator = Paginator(carts,20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'page_obj':page_obj,
        'carts':carts
    }
    return render(request,"orders.html",context)







@user_passes_test(lambda u: u.has_perm('order.can_access_produce_section'),login_url='/adminlte/login')
def produce_bread(request):
    carts=Cart.objects.filter(payment_date__date=timezone.now().date())
    cart=Cart.objects.filter(status__in=['2',"3"]).first()
    context={
        'carts':carts,
        'cart':cart,
    }
    return render(request,'produce_bread.html',context)


@user_passes_test(lambda u: u.has_perm('auth.change_user'),login_url='/adminlte/login')
def edite_user(request,id):
    user=User.objects.filter(id=id).first()
    if user is None:
        messages.success(request,'کاربری یافت نشد شاید حذف شده باشد ')
        return redirect('/adminlte/users')
    user_detail=User_detail.objects.get(user=user)
    form=User_Form(request.POST or None,instance=user)
    form2=User_Detail_Form(request.POST or None,request.FILES or None,instance=user_detail)
    if form.is_valid() and form2.is_valid():
        form.save()
        form2.save()
        messages.success(request,'ویرایش شد ')
        return redirect('/adminlte/users')
    context={
        'form':form,
        'form2':form2,
    }
    return render(request,'user_edite.html',context)



def validate_username(username):
    if re.search(r"^09\d{9}$",username) is None:
        raise FieldError("شماره تلفن معتبر نیست ")
    else:
        return None


@user_passes_test(lambda u: u.has_perm('auth.add_user'),login_url='/adminlte/login')
def add_user(request):
    form=User_Form(request.POST or None)
    form2=User_Detail_Form(request.POST or None,request.FILES or None)
    if form.is_valid() and form2.is_valid():
        user=form.save(commit=False)
        password = form.cleaned_data.get('password')
        username = form.cleaned_data['username']
        try:
            validate_password(password,user)
            validate_username(username=username)
            user.set_password(password)
            user.save()
            user_detail=form2.save(commit=False)
            user_detail.user=user
            user_detail.save()
            messages.success(request,'کاربر ایجاد شد ')
            return redirect('/adminlte/users')
        except ValidationError as e:
            form.add_error('password',e)
        except FieldError as e:
            form.add_error('username',e)
    context={
        'form':form,
        'form2':form2,
    }
    return render(request,'add_user.html',context)

@user_passes_test(lambda u: u.has_perm('auth.view_user'),login_url='/adminlte/login')
def user_list(request):
    users=User.objects.all()
    if request.GET.get('is_admin') :
       users=users.filter(is_staff=True)
    if  request.GET.get('is_superuser') :
       users=users.filter(is_superuser=True)
    paginator = Paginator(users,20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    admins=len(User.objects.filter(is_staff=True))
    context={
        'users':users,
        'page_obj':page_obj,
        'admin_num':admins
    }
    return render(request,'user_list.html',context)



@user_passes_test(lambda u: u.has_perm('bread.change_bread'),login_url='/adminlte/login')
def edite_bread(request,id):
    form=Bread_Form(request.POST or None ,request.FILES or None,instance=Bread.objects.get(id=id))
    if form.is_valid():
        form.save()
        messages.success(request,'نان با موفیت ویرایش شد ')
        return redirect('/adminlte/bread')
    context={
        'form':form,
    }
    return render(request,'bread_edite.html',context)


@user_passes_test(lambda u: u.has_perm('bread.add_bread'),login_url='/adminlte/login')
def add_bread(request):
    form=Bread_Form(request.POST or None ,request.FILES or None )
    if form.is_valid():
        form.save()
        messages.success(request,'نان با موفقیت اضافه شد ')
        return redirect('/adminlte/bread')
    context={
        'form':form,
    }
    return render(request,'bread_add.html',context)


@user_passes_test(lambda u: u.has_perm('bread.view_bread'),login_url='/adminlte/login')
def show_bread_list(request):
    breads=Bread.objects.all()
    context={
        'breads':breads,
    }
    return render(request,"bread_list.html",context)


@user_passes_test(lambda u: u.is_staff,login_url='/adminlte/login')
def dashboard(request):
    bread_num=len(Bread.objects.all())
    cart_num=len(Cart.objects.all())
    users=User.objects.all().order_by('-date_joined')[:8]
    carts=Cart.objects.all().order_by('-payment_date')[:6]
    context={
        'users':users,
        'carts':carts,
        'bread_num':bread_num,
        'cart_num':cart_num,
    }
    return render(request,'dashbord.html',context)





@user_passes_test(lambda u: u.is_superuser,login_url='/adminlte/login')
def switch_render(request):
    setting=Setting.objects.all().first()
    context={
        'is_on':setting.is_on
    }
    return render(request,'switch_render.html',context)



######################  APIs ##################################


class Get_SEll_Data(APIView):
    def get(self,request):
        jdatetime_now=jdatetime.datetime.now()
        start=jdatetime.date(jdatetime_now.year,1,1).togregorian()
        end=jdatetime.date(jdatetime_now.year,12,29)
        if end.isleap():
            end=end.togregorian()+timezone.timedelta(days=1)
        else:
            end=end.togregorian()
        c=Cart.objects.filter(is_paid=True,payment_date__range=[start,end]).order_by('payment_date')
        dictvalue={
            'فروردین':0,
            'اردیبهشت':0,
            'خرداد':0,
            'تیر':0,
            'مرداد':0,
            'شهریور':0,
            'مهر':0,
            'آبان':0,
            'آذر':0,
            'دی':0,
            'بهمن':0,
            'اسفند':0,
        }
        for i in c:
            month=datetime2jalali(i.payment_date).strftime('%B')
            dictvalue[month]=dictvalue[month]+1
        dict_value=dict(list(dictvalue.items())[0:jdatetime_now.month])
        context={
            'lables':dict_value.keys(),
            'values':dict_value.values(),
        }
        return Response(context,status=status.HTTP_200_OK)


class turn_off_or_on(APIView):
    permission_classes = (permissions.IsAuthenticated,Setting_Permission)

    def put(self, request):
        is_on=request.data.get('is_on')
        setting=Setting.objects.all().first()
        setting.is_on=bool(int(is_on))
        setting.save()
        return Response(status=status.HTTP_200_OK)


class Send_Order(APIView):
    permission_classes = (permissions.IsAuthenticated,Read_Only,Is_View_Cart)

    def get(self,request):
        cart=Cart.objects.filter(status__in=['2',"3"]).first()
        context={
                'cart':cart,
        }
        if cart is None:
            html="""
                        <div  style='display:flex;justify-content:center'>
                    <svg viewBox="0 0 100 100" style='width:300px;height:60px;margin-top:20px'  >
                        <defs>
                        <filter id="shadow">
                            <feDropShadow dx="0" dy="0" stdDeviation="1.5" 
                            flood-color="#fc6767"/>
                        </filter>
                        </defs>
                        <circle id="spinner" style="fill:transparent;stroke:#dd2476;stroke-width: 7px;stroke-linecap: round;filter:url(#shadow);" cx="50" cy="50" r="45"/>
                    </svg>
                    <br>
                    </div>
                    <h4 style='text-align:center;' class='mb-3' id='elemId'>سفارشی پیدا نشد !  درحال بارگیری</h4>
                    <br>
                """
            return Response({'html':html},status=status.HTTP_404_NOT_FOUND)
        rendered = render_to_string('change_status.html', context)
        return Response({'html':rendered},status=status.HTTP_200_OK)






class Change_Status(APIView):
    permission_classes = (permissions.IsAuthenticated,Change_Cart_Permisson)
    def post(self,request):
        cart_id=request.data.get('order_id')
        status_cart=request.data.get('status')
        cart=Cart.objects.filter(id=cart_id).first()
        cart.status=status_cart
        cart.save()
        if cart.status=='3':
            print('sms ersanl shode')
            return Response(status=status.HTTP_200_OK)
        elif cart.status=='4':
            phone=cart.user.username
            if cart.delivery_mode == '1':
                message="""
                نانوی شاپ
                نان شما تولید شد 
                در اسرع وقت به مغازه مراجعه کنید
                """
            else:
                message="""
                نانوی شاپ
                نان شما تولید شد 
                در اسرع وقت  توسط پیک برای شما ارسال میشود
                """
            send_message(phone,message)
            cart=Cart.objects.filter(status__in=['2',"3"]).first()
            if cart is None:
                html="""
                        <div  style='display:flex;justify-content:center'>
                    <svg viewBox="0 0 100 100" style='width:300px;height:60px;margin-top:20px'  >
                        <defs>
                        <filter id="shadow">
                            <feDropShadow dx="0" dy="0" stdDeviation="1.5" 
                            flood-color="#fc6767"/>
                        </filter>
                        </defs>
                        <circle id="spinner" style="fill:transparent;stroke:#dd2476;stroke-width: 7px;stroke-linecap: round;filter:url(#shadow);" cx="50" cy="50" r="45"/>
                    </svg>
                    <br>
                    </div>
                    <h4 style='text-align:center;' class='mb-3' id='elemId'>سفارشی پیدا نشد !  درحال بارگیری</h4>
                    <br>
                """
                return Response({'html':html},status=status.HTTP_404_NOT_FOUND)
            context={
                'cart':cart,
            }
            rendered = render_to_string('change_status.html', context)
            return Response({'html':rendered},status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)



class Delete_Discount_Item(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self,request):
        print(request.data)
        items=request.data.getlist('items[]')
        Discount.objects.filter(id__in=[int(i) for i in items]).delete()
        return Response(status=status.HTTP_200_OK)


class Delete_User_Item(APIView):
    permission_classes = (permissions.IsAuthenticated,User_Delete_Permission)

    def delete(self,request):
        items=request.data.getlist('items[]')
        User.objects.filter(id__in=[int(i) for i in items]).delete()
        return Response(status=status.HTTP_200_OK)



class Delete_Bread_Item(APIView):
    permission_classes = (permissions.IsAuthenticated,Bread_permission)

    def delete(self,request):
        items=request.data.getlist('items[]')
        breads=Bread.objects.filter(id__in=[int(i) for i in items]).delete()
        return Response(status=status.HTTP_200_OK)


def get_farsi_text(text):
        if reshaper.has_arabic_letters(text):
          words = text.split()
          reshaped_words = []
          for word in words:
            if reshaper.has_arabic_letters(word):
              # for reshaping and concating words
              reshaped_text = reshaper.reshape(word)
              # for right to left    
              bidi_text = get_display(reshaped_text)
              reshaped_words.append(bidi_text)
            else:
              reshaped_words.append(word)
          reshaped_words.reverse()
          return ' '.join(reshaped_words)
        return text

def get_farsi_bulleted_text(text, wrap_length=None):
       farsi_text = get_farsi_text(text)
       if wrap_length:
           line_list = textwrap.wrap(farsi_text, wrap_length)
           line_list.reverse()
           line_list[0] = '{};'.format(line_list[0])
           farsi_text = '<br/>'.join(line_list)
           return '<font>%s</font>' % farsi_text
       return '<font>%s</font>' % farsi_text

def get_farsi_bulleted_text2(text, wrap_length=None):
      farsi_text = get_farsi_text(text)
      if wrap_length:
           line_list = textwrap.wrap(farsi_text, wrap_length)
           line_list.reverse()
           line_list[0] = '{}'.format(line_list[0])
           farsi_text = ''.join(line_list)
           return '%s' %farsi_text
      return '%s' %farsi_text

def generate_pdf(buffer,object,path):
    pdfmetrics.registerFont(TTFont('Persian',path))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT, fontName='Persian', fontSize=9)) 
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT, fontName='Persian', fontSize=9)) 
    Story = []
    data= [
    [get_farsi_bulleted_text2('قیمت'),get_farsi_bulleted_text2('مقدار'), get_farsi_bulleted_text2('نام محصول ')],
    ]
    
    for i in object.cart_item.all():
        data.append([intcomma(i.bread.price*i.quantity,False),i.quantity,get_farsi_bulleted_text2(i.bread.title)])

    column_number=len(data)-1
    height_size=75+(column_number*20)
    doc = SimpleDocTemplate(buffer, pagesize=(78*mm,height_size*mm),  rightMargin=5, leftMargin=5, topMargin=10,
                        bottomMargin=10)
    doc.strokeColor = colors.green
    t=Table(data,colWidths=67,rowHeights=50)
    t.setStyle(TableStyle(
    [
    ('BACKGROUND',(0, 0), (-1, 0),colors.gray),
    ('TEXTCOLOR',(0,0),(1,-1),colors.black),
    ('FONT',(0,0),(-1,-1),'Persian'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]
    )
    )
    t.hAlign = 'RIGHT'
    tw = get_farsi_bulleted_text(f'نام و نام خانوادگی :{object.user.get_full_name()}')
    p = Paragraph(tw, styles['Right'])
    Story.append(p)
    Story.append(Spacer(1,5))
    tw = get_farsi_bulleted_text(f'شماره تلفن: {object.user.username}')
    p = Paragraph(tw, styles['Right'])
    Story.append(p)
    Story.append(Spacer(1,5))
    tw = get_farsi_bulleted_text(f'نوع تحویل: {object.get_delivery_mode_display()}')
    p = Paragraph(tw, styles['Right'])
    Story.append(p)
    Story.append(Spacer(1,10))
    Story.append(HRFlowable(width="100%", thickness=0.1, lineCap='round', color=colors.gray, spaceBefore=1, spaceAfter=1, hAlign='CENTER', vAlign='BOTTOM'))
    Story.append(Spacer(1, 10))
    Story.append(t)
    Story.append(Spacer(1, 15))
    Story.append(Spacer(1, 20))
    tw = get_farsi_bulleted_text(f'جمع خرید : {intcomma(object.cart_total_price(),False)}')
    p = Paragraph(tw, styles['Left'])
    Story.append(p)
    Story.append(Spacer(1, 4))
    tw = get_farsi_bulleted_text(f'تاریخ پرداخت : {datetime2jalali(object.payment_date).strftime("%H:%M  %Y/%m/%d") }')
    p = Paragraph(tw, styles['Left'])
    Story.append(p)
    doc.build(Story)

def report_pdf(request,id):
    path=os.path.join(BASE_DIR,'static_cdn\\static_roots\\font','IRANYekanLight.ttf')
    buffer = io.BytesIO()
    order=Cart.objects.filter(id=id).first()
    generate_pdf(buffer,order,path)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'order_receipt{order.id}.pdf')


def get_the_last_of_month_day(month,leap_year=False):
    months={
        1:'31',
        2:'31',
        3:'31',
        4:'31',
        5:'31',
        6:'31',
        7:'30',
        8:'30',
        9:'30',
        10:'30',
        11:'30',
        12:'29',
    }
    if leap_year: 
        months[12]='30'
    return int(months[month])


def report_exel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.xls"'
    day=request.GET.get('by_day')
    month=request.GET.get('by_month')
    year=request.GET.get('by_year')
    current_date_time=timezone.now()
    jalali_datetime_now=jdatetime.datetime.now()
    start=jdatetime.date(jalali_datetime_now.year,1,1).togregorian()
    end=jdatetime.date(jalali_datetime_now.year,12,29)
    month_start=jdatetime.date(jalali_datetime_now.year , jalali_datetime_now.month , 1).togregorian()
    month_end=jdatetime.date(jalali_datetime_now.year , jalali_datetime_now.month ,get_the_last_of_month_day(jalali_datetime_now.month,jalali_datetime_now.isleap())).togregorian()
    if end.isleap():
        end=end.togregorian()+timezone.timedelta(days=1)
    else:
        end=end.togregorian()
    if day:
        orders=Cart.objects.filter(payment_date__date=current_date_time.date())
        message=f'خروجی سفارش امروز {datetime2jalali(current_date_time).strftime("%Y/%m/%d")}' 
    elif month:
        orders=Cart.objects.filter(payment_date__range=[month_start,month_end])
        message=f'خروجی سفارش های این ماه {datetime2jalali(current_date_time).strftime("%Y/%m")}'
    elif year:
        orders=Cart.objects.filter(payment_date__range=[start,end]).order_by('payment_date')
        message=f'خروجی سفارش های سال {datetime2jalali(current_date_time).strftime("%Y" )}'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('orders')
    xlwt.add_palette_colour("custom_colour", 0x21)
    wb.set_colour_RGB(0x21,215,240,237 )
    row_num = 1
    font_style = xlwt.XFStyle()
    font_style.font.bold=True
    borders = xlwt.Borders()
    borders.left = borders.DOTTED
    borders.right = borders.DOTTED
    borders.top = borders.DOTTED
    borders.bottom = borders.DOTTED
    align = xlwt.Alignment()
    align.horz = xlwt.Alignment.HORZ_CENTER
    align.vert = xlwt.Alignment.VERT_CENTER
    fnt3 = xlwt.Font()
    fnt3.name = 'Arial'
    fnt3.height = 12*20
    fnt3.style= 'Regular'
    font_style.font=fnt3
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['custom_colour']




    font_style.pattern = pattern
    font_style.alignment=align
    font_style.borders=borders
    ws.cols_right_to_left = True
    ws.write_merge(0, 0,0, 3, message,font_style)
    columns = ['شماره سفارش', 'اسم', 'نام خانوادگی','تاریخ پرداخت']
    ws.row(0).height_mismatch = True
    ws.row(0).height = 700
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num],font_style)
        ws.col(col_num).width = 5000

    ws.row(1).height_mismatch = True
    ws.row(1).height = 600
    objects=[]
    for i in orders:
        ids=i.id
        first_name=i.user.first_name
        last_name=i.user.last_name
        payment_date=datetime2jalali(i.payment_date).strftime("%H:%M  %Y/%m/%d")
        tp=(ids,first_name,last_name,payment_date)
        objects.append(tp)
    for row in objects:
        row_num +=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num],font_style)
        
        ws.row(row_num).height_mismatch = True
        ws.row(row_num).height = 400

    wb.save(response)
    return response
