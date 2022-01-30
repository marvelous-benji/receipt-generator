

from rest_framework import serializers

from .models import ReceiptHistory
from MyUser.serializers import UserSerializer
from MyUser.models import CustomUser




class HistorySerializer(serializers.ModelSerializer):

	issued_by = UserSerializer()

	class Meta:
	    model = ReceiptHistory
	    fields = [
	    	'receipt_id',
	    	'date_issued',
	    	'issued_by',
	    	'payment_type',
	    	'payment_amount',
	    	'customer_phone_number',
			'customer_name',
	    	'payment_detail'
	    ]


	def is_valid(self, raise_Exception=False):

		'''
		Overiding the is_valid method of the serializer class
		is neccessary as it raises uniqueness error in nested
		relationship validation as it would normally do if
		it was checking uniqueness constraint in the creation
		of the parent object
		'''

		if self.instance is not None:
			return super().is_valid()
		self._validated_data = self.initial_data
		self._errors = {}
		return True

	def create(self, validated_data):
		issuer = self.context['request'].user
		receipts = [ReceiptHistory(
			date_issued=data['date_issued'],
			issued_by=issuer,
			receipt_id=data['receipt_id'],
			customer_name=data['customer_name'],
			customer_phone_number=data['customer_phone_number'],
			payment_amount=data['payment_amount'],
			payment_detail=data['payment_detail']
		) for data in validated_data]

		ReceiptHistory.objects.bulk_create(receipts)
		return receipts

	def update(self, instance, validated_data):

		instance.customer_name = validated_data.get('customer_name', instance.customer_name)
		instance.customer_phone_number = validated_data.get('customer_phone_number', instance.customer_phone_number)
		instance.payment_type = validated_data.get('payment_type', instance.payment_type)
		instance.payment_amount = validated_data.get('payment_amount', instance.payment_amount)
		instance.payment_detail = validated_data.get('payment_detail', instance.payment_detail)
		instance.save()
		return instance

