from django.db import models


class Account(models.Model):
    save_date = models.DateField()
    detail_text = models.CharField(max_length=200)
    income = models.FloatField(default=0)
    expenses = models.FloatField(default=0)
    balance = models.FloatField(default=0)
