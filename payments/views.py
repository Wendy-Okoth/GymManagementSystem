from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from members.models import Member

def payment_history(request):
    return HttpResponse("Payment history page coming soon!")

@csrf_exempt
def mpesa_callback(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        result_code = data['Body']['stkCallback']['ResultCode']

        phone_number = None
        items = data['Body']['stkCallback'].get('CallbackMetadata', {}).get('Item', [])
        for item in items:
            if item.get('Name') == 'PhoneNumber':
                phone_number = item.get('Value')

        if result_code == 0 and phone_number:
            member = Member.objects.filter(phone_number=phone_number).first()
            if member:
                member.has_paid = True
                member.save()

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Callback received successfully"})
    except Exception as e:
        return JsonResponse({"ResultCode": 1, "ResultDesc": f"Error: {str(e)}"})


