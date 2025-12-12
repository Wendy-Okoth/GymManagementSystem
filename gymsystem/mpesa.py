import requests
from requests.auth import HTTPBasicAuth
import os
import datetime
import base64

def get_mpesa_token():
    consumer_key = os.getenv("MPESA_CONSUMER_KEY")
    consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    json_response = response.json()
    return json_response['access_token']

def initiate_stk_push(phone_number, amount):
    access_token = get_mpesa_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    business_short_code = "174379"  # sandbox shortcode
    passkey = os.getenv("MPESA_PASSKEY")  # use env variable
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()

    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": business_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://yourdomain.com/mpesa/callback/",
        "AccountReference": "GymEncore",
        "TransactionDesc": "Membership Payment"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

