from datetime import datetime, timedelta
import requests
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .models import SentIPO
from subscriptions.models import Subscriber

def get_upcoming_ipos(request):
    api_key = "cvqk991r01qp88cm78e0cvqk991r01qp88cm78eg"
    today = datetime.today().date()
    from_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    to_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")

    url = f"https://finnhub.io/api/v1/calendar/ipo?from={from_date}&to={to_date}&token={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        ipo_data = response.json().get("ipoCalendar", [])

        upcoming = []
        recent = []
        newly_added = []

        for ipo in ipo_data:
            try:
                ipo_date = datetime.strptime(ipo["date"], "%Y-%m-%d").date()
                name = ipo.get("name", "")
                symbol = ipo.get("symbol", "")
                shares_raw = ipo.get("numberOfShares")
                shares = int(shares_raw.replace(",", "")) if shares_raw and isinstance(shares_raw, str) else int(shares_raw or 0)

                formatted_ipo = {
                    "name": name,
                    "symbol": symbol,
                    "date": ipo.get("date"),
                    "numberOfShares": shares,
                    "exchange": ipo.get("exchange"),
                    "price": ipo.get("price"),
                    "status": ipo.get("status"),
                }

                if ipo_date >= today:
                    upcoming.append(formatted_ipo)

                    if not SentIPO.objects.filter(symbol=symbol).exists():
                        newly_added.append(formatted_ipo)
                        SentIPO.objects.create(symbol=symbol, name=name)

                elif ipo_date >= today - timedelta(days=30):
                    recent.append(formatted_ipo)

            except Exception as e:
                print(f"Error formatting IPO entry: {e}")
                continue

        if newly_added:
            subject = "🚀 New IPOs Just Added!"
            ipo_lines = "\n\n".join([f"{ipo['name']} ({ipo['symbol']}) - {ipo['date']}" for ipo in newly_added])
            
            for email in Subscriber.objects.values_list('email', flat=True):
                unsubscribe_link = f"{settings.FRONTEND_URL}/unsubscribe/{email}"
                message = (
                    f"{ipo_lines}\n\n"
                    "You're receiving this email because you're subscribed to IPO alerts.\n"
                    f"If you'd like to unsubscribe, click here: {unsubscribe_link}"
                )
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                )

        recent_sorted = sorted(recent, key=lambda x: x["date"], reverse=True)

        return JsonResponse({
            "upcoming_ipos": upcoming,
            "recent_ipos": recent_sorted
        })

    except Exception as e:
        print(f"Error fetching IPOs from Finnhub: {e}")
        return JsonResponse({"error": str(e)}, status=500)
