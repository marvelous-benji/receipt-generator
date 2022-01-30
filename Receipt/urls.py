from django.urls import path, re_path

from . import views


urlpatterns = [
    path("receipt_template", views.ReceiptTemplate.as_view(), name="get_templates"),
    path("receipt_slips/<int:page>", views.ReceiptList.as_view(), name="issued_slips"),
    path(
        "receipt_edit/<str:receipt_id>", views.ReceiptDetail.as_view(), name="edit_slip"
    ),
    re_path(r"^.*/$", views.notfound), # catches all url starting with /api/v1/receipt but does not hit any endpoint
]
