import uuid

from django.utils import timezone
from django.db import models
from django.conf import settings

# Create your models here.

class ReceiptHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_issued = models.DateTimeField(default=timezone.now)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='history', on_delete=models.CASCADE)
    issued_to = models.CharField(max_length=200, null=False, blank=False)
    receipt_id = models.CharField(max_length=30,unique=True, blank=False)
    payment_type = models.CharField(max_length=15, blank=False, default='Cash')
    payment_amount = models.DecimalField(max_digits=52, decimal_places=2)
    payment_detail = models.TextField()

    def __str__(self):
        return self.receipt_id
