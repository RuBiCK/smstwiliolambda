import base64
import json
import os
from twilio.rest import Client
import logging
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.environ.get("TWILIO_FROM")
TWILIO_BODY = os.environ.get("TWILIO_BODY")

def parseNumber(phone_number):
    match = re.search(r'^[0-9]{9}$', phone_number)
    if match:
        parsedNumber = '+34' + phone_number
    else:
        return False
    return parsedNumber



def lambda_handler(event, context):
    logger.info(event)
    formNumber = event['data']['telefono']
    from_number = TWILIO_FROM
    smsbody = TWILIO_BODY

    to_number=parseNumber(formNumber)
    if to_number is False:
        return "Introduce un numero de telefono valido de nueve digitos"
    if not TWILIO_ACCOUNT_SID:
        return "Unable to access Twilio Account SID."
    elif not TWILIO_AUTH_TOKEN:
        return "Unable to access Twilio Auth Token."
    elif not to_number:
        return "The function needs a 'To' number in the format +34666777888"
    elif not from_number:
        return "The function needs a 'From' number in the format +34666777888"
    elif not smsbody:
        return "The function needs a 'Body' message to send."

    logger.info('Sending message from: ' + from_number + ' To: '  + to_number + ' Mensaje: ' + smsbody)
    try:
        client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)
        client.messages.create( from_=from_number, to=to_number, body=smsbody)
    except Exception as e:
        return e
    return "SMS sent successfully!"
