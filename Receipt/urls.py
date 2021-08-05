
from django.urls import path

from . import views


urlpatterns = [
    path('receipt_slips/', views.ReceiptSlip.as_view(), name='get_slips'),
    path('issue_receipt/', views.ReceiptIssuer.as_view(), name='issue_receipt'),
]
