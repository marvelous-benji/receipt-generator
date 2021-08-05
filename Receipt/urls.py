
from django.urls import path

from . import views


urlpatterns = [
    path('receipt_template/', views.ReceiptTemplate.as_view(), name='get_templates'),
    path('receipt_slips/', views.ReceiptList.as_view(), name='issued_slips'),
    path('receipt_edit/<str:receipt_id>', views.ReceiptDetail.as_view(), name='edit_slip')
]
