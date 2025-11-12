import requests
from django.conf import settings
import base64
from datetime import datetime

class MpesaClient:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.environment = settings.MPESA_ENVIRONMENT
        
    def get_access_token(self):
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(url, auth=(self.consumer_key, self.consumer_secret))
        return response.json()['access_token']
    
    def stk_push(self, phone_number, amount, account_reference, transaction_desc):
        access_token = self.get_access_token()
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            f"{self.shortcode}{self.passkey}{timestamp}".encode()
        ).decode('utf-8')
        
        headers = {"Authorization": f"Bearer {access_token}"}
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://yourdomain.com/api/mpesa/callback",
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }
        
        response = requests.post(url, json=payload, headers=headers)
        return response.json()