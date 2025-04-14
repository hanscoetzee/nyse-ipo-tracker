from django.core.mail import send_mail
from .models import Subscriber

def notify_all_subscribers(subject, message):
    recipients = Subscriber.objects.values_list('email', flat=True)
    if recipients:
        send_mail(
            subject,
            message,
            'no-reply@nyseipo.com',
            list(recipients),
            fail_silently=False
        )
