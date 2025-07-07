from django.db import models
from django.contrib.auth.models import User

class ConversionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=15, decimal_places=2)
    rate = models.DecimalField(max_digits=15, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} converted {self.amount} {self.from_currency} to {self.to_currency}"
