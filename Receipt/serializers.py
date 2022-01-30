from rest_framework import serializers

from .models import ReceiptHistory
from MyUser.serializers import UserSerializer
from MyUser.models import CustomUser


class HistorySerializer(serializers.ModelSerializer):

    issued_by = UserSerializer()

    class Meta:
        model = ReceiptHistory
        fields = [
            "receipt_id",
            "date_issued",
            "issued_by",
            "payment_type",
            "payment_amount",
            "customer_phone_number",
            "customer_name",
            "payment_detail",
        ]

    def is_valid(self, raise_Exception=False):

        """
        Overiding the is_valid method of the serializer class
        is neccessary as it raises uniqueness error in nested
        relationship validation as it would normally do if
        it was checking uniqueness constraint in the creation
        of the parent object
        """

        if self.instance is not None:
            self._errors = {}
            data = self.initial_data
            if data.get("payment_type", "Card") not in ["Cash", "Card", "Transfer"]:
                self._errors[
                    "payment_type"
                ] = "Only payment by Cash, Card and Transfer are available"
            if data.get("customer_phone_number", None):
                contact = data["customer_phone_number"]
                if not contact.startswith("+234") and len(contact) != 14:
                    self._errors[
                        "customer_phone_number"
                    ] = "Phone number must be valid and startswith +234"
            if data.get("payment_amount", None):
                amount = data["payment_amount"]
                if not isinstance(amount, (int, float)) or amount <= 0:
                    self._errors["payment_amount"] = "Payment amount is invalid"
            if data.get("customer_name", None):
                name = data["customer_name"]
                if not isinstance(name, str) or len(name) < 3:
                    self._errors["customer_name"] = "Customer name is invalid"
            if data.get("payment_detail", None):
                detail = data["payment_detail"]
                if not isinstance(detail, str):
                    self._errors["payment_detail"] = "Payment detail must be string"
            if self._errors:
                self._validated_data = {}
                return False
            self._validated_data = self.initial_data
            return True
        self._validated_data = dict(clean_data=self.initial_data)
        self._errors = {}
        return True

    def create(self, validated_data):
        issuer = self.context["request"].user
        receipts = [
            ReceiptHistory(
                date_issued=data["date_issued"],
                issued_by=issuer,
                customer_name=data["customer_name"],
                customer_phone_number=data["customer_phone_number"],
                payment_amount=data["payment_amount"],
                payment_detail=data["payment_detail"],
            )
            for data in validated_data["clean_data"]
        ]

        ReceiptHistory.objects.bulk_create(receipts)
        return receipts

    def update(self, instance, validated_data):

        instance.customer_name = validated_data.get(
            "customer_name", instance.customer_name
        )
        instance.customer_phone_number = validated_data.get(
            "customer_phone_number", instance.customer_phone_number
        )
        instance.payment_type = validated_data.get(
            "payment_type", instance.payment_type
        )
        instance.payment_amount = validated_data.get(
            "payment_amount", instance.payment_amount
        )
        if not validated_data.get("payment_detail", None):
            instance.payment_detail = f"""{instance.customer_name} bought goods worth {instance.payment_amount} Naira on {instance.date_issued.strftime("%d %b %Y %H:%M:%S")}"""
        else:
            instance.payment_detail = validated_data.get(
                "payment_detail", instance.payment_detail
            )
        instance.save()
        return instance
