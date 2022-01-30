from random import choice
from secrets import token_hex
import uuid

from django.utils import timezone
from django.db import models
from django.conf import settings

# Create your models here.

def get_payment_type():
    return choice(['Cash','Transfer','Card'])

def set_receipt_id():
    return token_hex(10)

class ReceiptHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_issued = models.DateTimeField(default=timezone.now)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='history', on_delete=models.CASCADE)
    receipt_id = models.CharField(max_length=30,unique=True, db_index=True, default=set_receipt_id)
    payment_type = models.CharField(max_length=15, default=get_payment_type)
    customer_phone_number = models.CharField(max_length=15)
    customer_name = models.CharField(max_length=100, db_index=True)
    payment_amount = models.DecimalField(max_digits=52, decimal_places=2)
    payment_detail = models.TextField()

    def __str__(self):
        return self.receipt_id
