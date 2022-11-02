# import string
# import random

# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.lib.enums import TA_RIGHT,TA_LEFT
# from reportlab.pdfbase import pdfmetrics
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle 
# from bidi.algorithm import get_display
# from rtl import reshaper
# import textwrap
# import datetime
# from  reportlab.lib import  pagesizes
# from reportlab.platypus import SimpleDocTemplate, Paragraph,Table, TableStyle,Spacer
# from reportlab.lib import colors



# def get_farsi_text(text):
#         if reshaper.has_arabic_letters(text):
#           words = text.split()
#           reshaped_words = []
#           for word in words:
#             if reshaper.has_arabic_letters(word):
#               # for reshaping and concating words
#               reshaped_text = reshaper.reshape(word)
#               # for right to left    
#               bidi_text = get_display(reshaped_text)
#               reshaped_words.append(bidi_text)
#             else:
#               reshaped_words.append(word)
#           reshaped_words.reverse()
#           return ' '.join(reshaped_words)
#         return text

# def get_farsi_bulleted_text(text, wrap_length=None):
#        farsi_text = get_farsi_text(text)
#        if wrap_length:
#            line_list = textwrap.wrap(farsi_text, wrap_length)
#            line_list.reverse()
#            line_list[0] = '{};'.format(line_list[0])
#            farsi_text = '<br/>'.join(line_list)
#            return '<font>%s</font>' % farsi_text
#        return '<font>%s</font>' % farsi_text

# def get_farsi_bulleted_text2(text, wrap_length=None):
#       farsi_text = get_farsi_text(text)
#       if wrap_length:
#            line_list = textwrap.wrap(farsi_text, wrap_length)
#            line_list.reverse()
#            line_list[0] = '{}'.format(line_list[0])
#            farsi_text = ''.join(line_list)
#            return '%s' %farsi_text
#       return '%s' %farsi_text

# pdfmetrics.registerFont(TTFont('Persian',r'C:\Users\rezak\Desktop\python\bakeshop\static_cdn\static_roots\font\IRANYekanLight.ttf'))
# styles = getSampleStyleSheet()
# styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT, fontName='Persian', fontSize=10)) 
# styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT, fontName='Persian', fontSize=10)) 
# doc = SimpleDocTemplate("farsi_wrap.pdf", pagesize=pagesizes.A6,  rightMargin=10, leftMargin=10, topMargin=65,
#                     bottomMargin=18)
# Story = []
# doc.strokeColor = colors.green
# data= [
# (get_farsi_bulleted_text2('تعداد'), get_farsi_bulleted_text2('نام محصول ')),
# (get_farsi_bulleted_text2('5'), get_farsi_bulleted_text2('سنگک')),
# (get_farsi_bulleted_text2('5'), get_farsi_bulleted_text2('سنگگ ابی')),
# ]

# t=Table(data,colWidths=130,rowHeights=50)
# t.setStyle(TableStyle(
# [
# ('BACKGROUND',(0,0),(-1,-2),colors.gray),
# ('TEXTCOLOR',(0,0),(1,-1),colors.black),
# ('FONT',(0,0),(-1,-1),'Persian'),
# ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
# ('ALIGN',(0,0),(-1,-1),'CENTER'),
# ('ALIGN',(0,0),(-1,-1),'CENTER'),
# ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
# ]
# )
# )
# t.hAlign = 'RIGHT'
# tw = get_farsi_bulleted_text('نام و نام خانوادگی : رضا خلیلیان عادل')
# p = Paragraph(tw, styles['Right'])
# Story.append(p)
# Story.append(Spacer(1,5))
# tw = get_farsi_bulleted_text('شماره تلفن: 09150521364')
# p = Paragraph(tw, styles['Right'])
# Story.append(p)
# Story.append(Spacer(1,5))

# tw = get_farsi_bulleted_text('نوع تحویل: حضوری')
# p = Paragraph(tw, styles['Right'])
# Story.append(p)

# # Story.append(p)
# Story.append(Spacer(1, 20))
# Story.append(t)
# Story.append(Spacer(1, 20))
# Story.append(Spacer(1, 20))

# tw = get_farsi_bulleted_text('جمع خرید : 138,254')
# p = Paragraph(tw, styles['Left'])
# Story.append(p)
# Story.append(Spacer(1, 4))
# tw = get_farsi_bulleted_text(f'تاریخ پرداخت : {datetime.datetime.now()}')
# p = Paragraph(tw, styles['Left'])
# Story.append(p)
# doc.build(Story)


# def generate_unique_code(length:int) -> str:
#     "generate unique code " 
#     unique_code=''
#     char_number_symbols=string.ascii_letters+string.digits
#     for i in range(0,length):
#         unique_code+=random.choice(char_number_symbols)
#     return unique_code


# print(generate_unique_code(16))



# from colorama import Fore, Back, Style


# user_rate=0
# bot_rate=0
# print('rock is 1 , paper is 2 , scissors is 3')
# while True:
#     if bot_rate==3 or user_rate==3:
#         break 
#     user_number=int(input("enter your number : "))
#     robot_choice=random.choice([1,2,3])
#     print(f'robot choice is {robot_choice}')
#     if user_number==3 and robot_choice==1:
#         bot_rate+=1
#     elif user_number==1 and robot_choice==3:
#         user_rate+=1
#     elif user_number==3 and robot_choice==2:
#         user_rate+=1
#     elif user_number==2 and robot_choice==3:
#         bot_rate+=1
#     elif user_number==1 and robot_choice==2:
#         bot_rate+=1
#     elif user_rate==2 and robot_choice==1:
#         user_rate+=1
    
# print(f'bot rate is {bot_rate} your rate is {user_rate}')
# if bot_rate>user_rate:
#     print(Fore.RED+'bot win')
# else:
#     print(Fore.GREEN+'user win')

# print(Style.RESET_ALL)

# s=input('enter your word : ')
# text=s.replace(' ','').lower()
# letter=''
# count=0
# for i in text:
#     c=text.count(i)
#     if c>=count:
#         letter=i
#         count=c
# print(f'letter  {letter}')
# print(f'count  {count}' )
     
       

