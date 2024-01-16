import random
from sms_configure.restapi import restfulapi
from os import getenv
import requests

# Password=mohammadi1368&PatternCodeID=391&PatternValues=40102&Mobile=09150521364

def send_message(phone_number,message):
    payload = {
        'UserName': '09153199038',
        'Password':'mohammadi1368',
        'PatternCodeID':'391',
        'PatternValues':message,
        'Mobile':phone_number,
        }
    r = requests.get('https://amootsms.com/webservice2.asmx/SendWithPattern', params=payload)
    return r.status_code
    

