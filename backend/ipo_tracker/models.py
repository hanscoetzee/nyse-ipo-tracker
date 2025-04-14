from django.db import models

class IPO(models.Model):
    company_name = models.CharField(max_length=100)
    listing_date = models.DateField()
    stock_symbol = models.CharField(max_length=10)
    exchange = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.company_name} ({self.stock_symbol})"

class SentIPO(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.name}"