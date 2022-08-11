import random
from sms_configure.restapi import restfulapi

def send_message(phone_number,message):
    phonenumber = "5000299556828"
    groupId = random.randint(0, 99999999)
    ws = restfulapi("rezakhalillian","reza1380")
    ws.SendMessage(PhoneNumber=phonenumber,Message=message,Mobiles=[phone_number],UserGroupID=str(groupId),SendDateInTimeStamp=1558298601)


