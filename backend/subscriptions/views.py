from django.http import JsonResponse
from .models import Subscriber
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import json

@csrf_exempt
def subscribe_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({"message": "Already subscribed."})

            # Create new subscriber
            Subscriber.objects.create(email=email)

            # Send welcome email
            subject = "🎉 Welcome to NYSE IPO Alerts!"
            message = (
                "Hi there,\n\n"
                "Thanks for subscribing to NYSE IPO alerts!\n\n"
                "We'll notify you whenever a new IPO is added to the upcoming list.\n\n"
                "If you ever want to unsubscribe, simply click the unsubscribe link "
                "included in every email.\n\n"
                "To the moon 🚀!"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return JsonResponse({"message": "Subscribed successfully!"})
        
        except Exception as e:
            print(f"Subscription error: {e}")
            return JsonResponse({"error": "Something went wrong."}, status=500)
    
    return JsonResponse({"error": "Invalid request method."}, status=405)

from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse

def unsubscribe(request, uidb64):
    try:
        email = urlsafe_base64_decode(uidb64).decode()
        subscriber = Subscriber.objects.get(email=email)
        subscriber.delete()
        return HttpResponse("You have successfully unsubscribed.")
    except Exception as e:
        return HttpResponse("Invalid unsubscribe link.")

from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from .models import Subscriber

def unsubscribe_user(request, uidb64):
    try:
        email = urlsafe_base64_decode(uidb64).decode()
        subscriber = Subscriber.objects.get(email=email)
        subscriber.delete()
        return HttpResponse("You have successfully unsubscribed.")
    except Exception as e:
        return HttpResponse("Invalid unsubscribe link.")
