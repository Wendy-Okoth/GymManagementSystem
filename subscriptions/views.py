from django.http import HttpResponse

def subscription_list(request):
    return HttpResponse("Subscriptions list page coming soon!")

def subscription_detail(request, id):
    return HttpResponse(f"Subscription detail page for subscription {id}")
