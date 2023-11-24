import random
from sms_configure.restapi import restfulapi
from os import getenv


def send_message(phone_number,message):
    phonenumber = getenv('PHONENUMBER')
    groupId = random.randint(0, 99999999)
    ws = restfulapi(getenv('SMSUSERNAME'),getenv('SMSPASSWORD'))
    ws.SendMessage(PhoneNumber=phonenumber,Message=message,Mobiles=[phone_number],UserGroupID=str(groupId),SendDateInTimeStamp=1558298601)


