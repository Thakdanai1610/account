from django.db import models


class Account(models.Model):
    save_date = models.DateField()
    detail_text = models.CharField(max_length=200)
    money = models.FloatField(default=0)
    money_type = models.CharField(max_length=8)
    balance = models.FloatField(default=0)
