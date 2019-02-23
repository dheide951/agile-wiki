from django.db import models


class Donation(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    invoice = models.CharField(max_length=50, null=True)